import inspect
import sys
import types
from pydoc import locate

from core.constants import *

def is_iterable(obj):
    return hasattr(obj, '__iter__') and hasattr(obj, '__next__') and callable(obj.__iter__)
def get_type(item):
    item_type = str(type(item))
    return item_type[8:len(item_type) - 2]


class Serializer:

    def serialize(self, obj):
        if isinstance(obj, (int, float, complex, bool, str, type(None))):
            return self.serialize_single_var(obj)
        elif isinstance(obj, (list, tuple, set, bytes, bytearray)):
            return self.serialize_collection(obj)
        elif isinstance(obj, dict):
            return self.serialize_dict(obj)
        elif inspect.isfunction(obj):
            return self.serialize_function(obj)
        elif inspect.isclass(obj):
            return self.serialize_class(obj)
        elif inspect.iscode(obj):
            return self.serialize_code(obj)
        elif inspect.ismodule(obj):
            return self.serialize_module(obj)
        elif inspect.ismethoddescriptor(obj) or inspect.isbuiltin(obj):
            return self.serialize_instance(obj)
        elif inspect.isgetsetdescriptor(obj) or inspect.ismemberdescriptor(obj):
            return self.serialize_instance(obj)
        elif isinstance(obj, type(type.__dict__)):
            return self.serialize_instance(obj)
        elif is_iterable(obj):
            return self.serialize_iterable(obj)
        else:
            return self.serialize_object(obj)

    def serialize_single_var(self, item):
        serialized_dict = {TYPE: get_type(item), VALUE: item}

        return serialized_dict

    def serialize_iterable(self, obj):
        # Convert the iterable object to a list for serialization
        serialized_items = [self.serialize(item) for item in obj]
        return {'type': ITERATOR, 'value': serialized_items}

    def serialize_collection(self, item):
        serialized_dict = {TYPE: get_type(item), VALUE: [self.serialize(obj) for obj in item]}

        return serialized_dict

    def serialize_dict(self, item):
        serialized_dict = {TYPE: get_type(item),
                           VALUE: [[self.serialize(key), self.serialize(item[key])] for key in item]}

        return serialized_dict

    def serialize_function(self, item):
        members = inspect.getmembers(item)
        serialized = dict()
        serialized['type'] = str(type(item))[8:-2]
        value = {}

        for name, val in members:
            if name in ["__code__", "__name__", "__defaults__", "__closure__"]:
                value[name] = val
            if name == "__code__":
                co_names = val.co_names
                globs = item.__globals__
                value["__globals__"] = {}

                for co_name in co_names:
                    if co_name == item.__name__:
                        value["__globals__"][co_name] = item.__name__
                    elif not inspect.ismodule(co_name) and co_name in globs:
                        value["__globals__"][co_name] = globs[co_name]

            if name == "__closure__":
                closure = val
                if closure:
                    closure_values = [cell.cell_contents for cell in closure]
                    value["__closure__"] = closure_values

        serialized["value"] = self.serialize(value)
        return serialized

    def serialize_class(self, item):
        serialized_dict = {TYPE: CLASS}
        value = {
            NAME: item.__module__ + '.' + item.__name__,
            MRO: [base.__module__ + '.' + base.__qualname__ for base in item.__bases__],
        }
        members = inspect.getmembers(item)
        for obj in members:
            if obj[0] not in NOT_CLASS_ATTRIBUTES:
                value[obj[0]] = self.serialize(obj[1])
        serialized_dict[VALUE] = self.serialize(value)

        return serialized_dict

    def serialize_code(self, item):
        if get_type(item) is None:
            return None

        members = inspect.getmembers(item)
        serialized_dict = {TYPE: get_type(item),
                           VALUE: self.serialize({obj[0]: obj[1] for obj in members if not callable(obj[1])})}

        return serialized_dict

    def serialize_module(self, item):
        temp_item = str(item)
        serialized_dict = {TYPE: get_type(item), VALUE: temp_item[9:len(temp_item) - 13]}

        return serialized_dict

    def serialize_instance(self, item):
        members = inspect.getmembers(item)
        serialized_dict = {TYPE: get_type(item),
                           VALUE: self.serialize({obj[0]: obj[1] for obj in members if not callable(obj[1])})}

        return serialized_dict

    def serialize_object(self, item):
        serialized_dict = {TYPE: OBJECT, VALUE: self.serialize({OBJECT_TYPE: type(item), FIELDS: item.__dict__})}

        return serialized_dict

    def deserialize(self, item):
        if item[TYPE] in [INT, FLOAT, BOOL, STRING, COMPLEX, NONE_TYPE]:
            return self.deserialize_single_var(item)
        elif item[TYPE] in [LIST, TUPLE, SET, BYTES, BYTE_ARRAY]:
            return self.deserialize_collection(item)
        elif item[TYPE] == DICT:
            return self.deserialize_dict(item)
        elif item[TYPE] == FUNCTION:
            return self.deserialize_function(item)
        elif item[TYPE] == CLASS:
            return self.deserialize_class(item)
        elif item[TYPE] == MODULE:
            return self.deserialize_module(item)
        elif item[TYPE] == OBJECT:
            return self.deserialize_object(item)
        elif item[TYPE] == ITERATOR:
            return self.deserialize_iterable(item)

    def deserialize_single_var(self, item):
        if item[TYPE] == NONE_TYPE:
            return None
        elif item[TYPE] == BOOL and isinstance(item[VALUE], str):
            return item[VALUE] == TRUE
        else:
            return locate(item[TYPE])(item[VALUE])

    def deserialize_iterable(self, item):
        serialized_items = item['value']
        return iter(self.deserialize(item) for item in serialized_items)

    def deserialize_collection(self, item):
        if item[TYPE] == LIST:
            return list(self.deserialize(obj) for obj in item[VALUE])
        elif item[TYPE] == TUPLE:
            return tuple(self.deserialize(obj) for obj in item[VALUE])
        elif item[TYPE] == SET:
            return set(self.deserialize(obj) for obj in item[VALUE])
        elif item[TYPE] == BYTES:
            return bytes(self.deserialize(obj) for obj in item[VALUE])
        elif item[TYPE] == BYTE_ARRAY:
            return bytearray(self.deserialize(obj) for obj in item[VALUE])

    def deserialize_dict(self, item):
        return {self.deserialize(obj[0]): self.deserialize(obj[1]) for obj in item[VALUE]}

    def deserialize_function(self, item):
        res_dict = self.deserialize(item['value'])
        closures = res_dict.get('__closure__')
        if closures is not None:
            closure_cells = []
            for cell_value in closures:
                cell = types.CellType(cell_value)
                closure_cells.append(cell)
            res_dict['closure'] = tuple(closure_cells)
        res_dict.pop('__closure__')

        res_dict['code'] = self.deserialize_code(item)
        res_dict.pop('__code__')

        res_dict['globals'] = res_dict['__globals__']
        res_dict.pop('__globals__')

        res_dict['name'] = res_dict['__name__']
        res_dict.pop('__name__')

        res_dict['argdefs'] = res_dict['__defaults__']
        res_dict.pop('__defaults__')

        res = types.FunctionType(**res_dict)
        if res.__name__ in res.__getattribute__('__globals__'):
            res.__getattribute__('__globals__')[res.__name__] = res

        return res

    def deserialize_code(self, item):
        items = item['value']['value']

        for tmp in items:
            if tmp[0]['value'] == '__code__':
                args = self.deserialize(tmp[1]['value'])
                code_dict = dict()
                for arg in args:
                    arg_val = args[arg]
                    if arg != '__doc__':
                        code_dict[arg] = arg_val
                code_list = [0] * 16

                for name in code_dict:
                    if name == 'co_lnotab':
                        continue
                    code_list[CODE_ARGS.index(name)] = code_dict[name]

                return types.CodeType(*code_list)

    def deserialize_class(self, item):
        class_dict = self.deserialize(item[VALUE])
        name = class_dict[NAME]
        mro_names = class_dict[MRO]
        del class_dict[NAME]
        del class_dict[MRO]

        mro = []
        for base_name in mro_names:
            module, _, cls_name = base_name.rpartition('.')
            base_cls = getattr(sys.modules[module], cls_name)
            mro.append(base_cls)

        cls = type(name, tuple(mro), class_dict)

        return cls
    def deserialize_module(self, item):
        return __import__(item[VALUE])

    # def deserialize_object(self, item):
    #     value = self.deserialize(item[VALUE])
    #
    #     if OBJECT_TYPE not in value or FIELDS not in value:
    #         raise ValueError("Invalid object serialization format")
    #
    #     object_type = value[OBJECT_TYPE]
    #     fields = value[FIELDS]
    #
    #     if object_type is None or not callable(object_type):
    #         raise ValueError("Invalid object type")
    #
    #     result = object_type.__new__(object_type)
    #
    #     for key, value in fields.items():
    #         setattr(result, key, self.deserialize(value))
    #
    #     return result

    def deserialize_object(self, obj):
        if TYPE not in obj or VALUE not in obj:
            raise ValueError("Invalid object serialization format")

        serialized_data = self.deserialize(obj[VALUE])

        if OBJECT_TYPE not in serialized_data or FIELDS not in serialized_data:
            raise ValueError("Invalid serialized object format")

        object_type = serialized_data[OBJECT_TYPE]
        fields = serialized_data[FIELDS]
        unpacked = object.__new__(object_type)
        unpacked.__dict__.update({key: self.deserialize(value) for key, value in fields.items()})

        return unpacked

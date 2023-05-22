import inspect
import re
import frozendict

from Lab3.core.constants import *


def get_type(item):
    item_type = str(type(item))

    return item_type[8:len(item_type) - 2]


class Serializer:
    def __init__(self, serialize_format):
        self.format = serialize_format

    def dump(self, obj, fp):
        pass

    def dumps(self, obj):
        pass

    def load(self, fp):
        pass

    def loads(self, s):
        pass

    def serialize(self, obj):
        if isinstance(obj, (int, float, complex, bool, str, type(None))):
            return self.serialize_single_var(obj)
        elif isinstance(obj, (list, tuple, set, bytes)):
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
        else:
            return self.serialize_object(obj)

    def serialize_single_var(self, item):
        serialized_dict = {TYPE: get_type(item), VALUE: item}

        return serialized_dict

    def serialize_collection(self, item):
        serialized_dict = {TYPE: get_type(item), VALUE: [self.serialize(obj) for obj in item]}

        return serialized_dict

    def serialize_dict(self, item):
        serialized_dict = {TYPE: get_type(item), VALUE: [[self.serialize(key), self.serialize(item[key])] for key in item]}

        return serialized_dict

    def serialize_function(self, item):
        members = inspect.getmembers(item)
        serialized = dict()
        serialized['type'] = str(type(item))[8:-2]
        value = dict()

        for tmp in members:
            if tmp[0] in ['__code__', '__name__', '__defaults__']:
                value[tmp[0]] = (tmp[1])
            if tmp[0] == '__code__':
                co_names = tmp[1].__getattribute__('co_names')
                globs = item.__getattribute__('__globals__')
                value['__globals__'] = dict()

                for tmp_co_names in co_names:
                    if tmp_co_names == item.__name__:
                        value['__globals__'][tmp_co_names] = item.__name__
                    elif not inspect.ismodule(tmp_co_names) \
                            and tmp_co_names in globs:
                        # and tmp_co_names not in __builtins__:
                        value['__globals__'][tmp_co_names] = globs[tmp_co_names]

        serialized['value'] = self.serialize(value)

        return serialized

    def serialize_class(self, item):
        serialized_dict = {TYPE: CLASS}
        value = {NAME: item.__name__}
        members = inspect.getmembers(item)
        for obj in members:
            if not (obj[0] in NOT_CLASS_ATTRIBUTES):
                value[obj[0]] = obj[1]
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

    def deserialize(self, s):
        pass

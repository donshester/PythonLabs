import types

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
        result = {}
        if isinstance(obj, (int, bool, str, float, complex, type(None))):
            result = self.serialize_primitive(obj)
        elif isinstance(obj, (list, set, tuple)):
            result = self.serialize_collection(obj)
        elif isinstance(obj, dict):
            result = self.serialize_dict(obj)
        elif callable(obj):
            result = self.serialize_function(obj)
        return result

    def serialize_primitive(self, obj):
        return {type(obj).__name__: obj}

    def serialize_collection(self, obj):
        tag = type(obj).__name__
        children = [self.serialize(item) for item in obj]
        return {tag: children}

    def serialize_dict(self, obj):
        tag = type(obj).__name__
        children = {}
        for key, value in obj.items():
            children[key] = self.serialize(value)
        return {tag: children}

    def serialize_function(self, obj):
        if obj.__closure__ and "__class__" in obj.__code__.co_freevars:
            closure = ([self.serialize(c.cell_contents) for c in obj.__closure__])
        else:
            closure = obj.__closure__

        items = {
            "argcount": self.serialize(obj.__code__.co_argcount),
            "posonlyargcount": self.serialize(obj.__code__.co_posonlyargcount),
            "kwonlyargcount": self.serialize(obj.__code__.co_kwonlyargcount),
            "nlocals": self.serialize(obj.__code__.co_nlocals),
            "stacksize": self.serialize(obj.__code__.co_stacksize),
            "flags": self.serialize(obj.__code__.co_flags),
            "code": self.serialize(obj.__code__.co_code),
            "consts": self.serialize(obj.__code__.co_consts),
            "names": self.serialize(obj.__code__.co_names),
            "varnames": self.serialize(obj.__code__.co_varnames),
            "filename": self.serialize(obj.__code__.co_filename),
            "name": self.serialize(obj.__code__.co_name),
            "firstlineno": self.serialize(obj.__code__.co_firstlineno),
            "lnotab": self.serialize(obj.__code__.co_lnotab),
            "freevars": self.serialize(obj.__code__.co_freevars),
            "cellvars": self.serialize(obj.__code__.co_cellvars),
            "globals": {
                k: self.serialize(v)
                for k, v in obj.__globals__.items()
                if isinstance(v, (types.ModuleType, str, int, float, bool))
            },
            "closure": self.serialize(obj.__closure__),
            "qualname": self.serialize(obj.__qualname__)
        }
        return {"__type__": "function", "items": items}


    def deserialize(self, s):
        pass


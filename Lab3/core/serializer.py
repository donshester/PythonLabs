from Lab3.core.serialize_helpers.serialize_helpers import serialize_primitive, serialize_collection


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
        if isinstance(obj, [int, bool, str, float, complex, type(None)]):
            result = self.serialize_primitive(obj)
        elif isinstance(obj, (list, set, tuple)):
            result = self.serialize_collection(obj)
        elif isinstance(obj, dict):
            result = self.serialize_dict(obj)
        elif callable(obj):
            return self.serialize_function(obj)
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
        pass
    def deserialize(self, s):
        pass


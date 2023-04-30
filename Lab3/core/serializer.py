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
        pass

    def deserialize(self, s):
        pass

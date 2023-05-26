from core.formats.json import JsonSerializer
from core.formats.xml import XmlSerializer


class Factory:
    @staticmethod
    def create_serializer(file_type):
        if file_type == "json":
            return JsonSerializer
        elif file_type == "xml":
            return XmlSerializer

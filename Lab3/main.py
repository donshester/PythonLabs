import argparse

from config import load_config
from core import Serializer
from core.factory import Factory
from core.formats.json.json import JsonSerializer
from core.formats.xml.xml import XmlSerializer

class A:
    def info_a(self):
        return 'a'


class B:
    def info_b(self):
        return 'b'


class BIGBIGBIG(A, B):
    def info_c(self):
        return self.info_a() + self.info_b() + 'c'

def main():
    ser = Factory.create_serializer('json')

    sered = ser.dumps(BIGBIGBIG())
    print(sered)
    a = ser.loads(sered)
    print(dir(a))


# def main():
#     parser = argparse.ArgumentParser(description="Serializer Utility")
#
#     parser.add_argument("--config", help="Path to the configuration file")
#     parser.add_argument("file_from", help="Path to the input file")
#     parser.add_argument("file_to", help="Path to the output file")
#     parser.add_argument("format_from", help="Input format (json/xml)")
#     parser.add_argument("format_to", help="Output format (json/xml)")
#
#     args = parser.parse_args()
#
#     if args.config:
#         file_from, file_to, format_from, format_to = load_config(args.config)
#     else:
#         file_from = args.file_from
#         file_to = args.file_to
#         format_from = args.format_from
#         format_to = args.format_to
#
#     serializer = Factory.create_serializer(format_from)
#
#     if format_to == "json":
#         if format_from == "json":
#             data = serializer.load(file_from)
#             serializer.dump(data, file_to)
#         elif format_from == "xml":
#             data = XmlSerializer.load(file_from)
#             JsonSerializer.dump(data, file_to)
#     elif format_to == "xml":
#         if format_from == "json":
#             data = JsonSerializer.load(file_from)
#             XmlSerializer.dump(data, file_to)
#         elif format_from == "xml":
#             data = serializer.load(file_from)
#             serializer.dump(data, file_to)
#
#     print("Operation completed successfully.")


if __name__ == '__main__':
    main()

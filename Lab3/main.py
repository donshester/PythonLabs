import argparse

from config import load_config
from core.factory import Factory
from core.serializers.jsonserializer import JSONSerializer
from core.serializers.xmlserializer import XMLSerializer

def main():
    parser = argparse.ArgumentParser(description="Serializer Utility")


    parser.add_argument("--config", help="Path to the configuration file")
    parser.add_argument("file_from", help="Path to the input file")
    parser.add_argument("file_to", help="Path to the output file")
    parser.add_argument("format_from", help="Input format (json/xml)")
    parser.add_argument("format_to", help="Output format (json/xml)")

    args = parser.parse_args()

    if args.config:
        file_from, file_to, format_from, format_to = load_config(args.config)
    else:
        file_from = args.file_from
        file_to = args.file_to
        format_from = args.format_from
        format_to = args.format_to

    serializer = Factory.create_serializer(format_from)

    if format_to == "json":
        if format_from == "json":
            data = serializer.load(file_from)
            serializer.dump(data, file_to)
        elif format_from == "xml":
            data = XMLSerializer.load(file_from)
            JSONSerializer.dump(data, file_to)
    elif format_to == "xml":
        if format_from == "json":
            data = JSONSerializer.load(file_from)
            XMLSerializer.dump(data, file_to)
        elif format_from == "xml":
            data = serializer.load(file_from)
            serializer.dump(data, file_to)

    print("Operation completed successfully.")


if __name__ == '__main__':
    main()

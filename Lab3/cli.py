from core.formats.json.json import JsonSerializer
from core.formats.xml.xml import XmlSerializer

while True:
    print('Enter 1 to load from JSON')
    print('Enter 2 to load from XML')
    print('Enter 3 to convert JSON to XML')
    print('Enter 4 to convert XML to JSON')
    print('Enter 5 to exit')

    choice = input("Choose an option: ")

    if choice == '1':
        json_filename = input('Enter JSON filename: ')
        try:
            obj = JsonSerializer.load(json_filename)
            print(obj)
        except FileNotFoundError:
            print('File not found.')
    elif choice == '2':
        xml_filename = input("Enter XML filename: ")
        try:
            obj = XmlSerializer.load(xml_filename)
            print(obj)
        except FileNotFoundError:
            print('File not found.')
    elif choice == '3':
        json_filename = input("Enter JSON filename: ")
        xml_filename = input('Enter XML filename: ')
        try:
            obj = JsonSerializer.load(json_filename)
            XmlSerializer.dump(obj, xml_filename)
            print('Conversion successful.')
        except FileNotFoundError:
            print('File not found.')
    elif choice == '4':
        xml_filename = input("Enter XML filename: ")
        json_filename = input('Enter JSON filename: ')
        try:
            obj = XmlSerializer.load(xml_filename)
            JsonSerializer.dump(obj, json_filename)
            print('Conversion successful.')
        except FileNotFoundError:
            print('File not found.')
    elif choice == '5':
        break
    else:
        print('Incorrect input. Try again.')

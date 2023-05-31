import configparser


def load_config(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)

    file_from = config.get("General", "file_from")
    file_to = config.get("General", "file_to")
    format_from = config.get("General", "format_from")
    format_to = config.get("General", "format_to")

    return file_from, file_to, format_from, format_to

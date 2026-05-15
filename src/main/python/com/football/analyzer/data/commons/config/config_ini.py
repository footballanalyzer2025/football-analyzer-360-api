import configparser


class ConfigIni:

    CONFIG_FILE_PATH = "deployment/config/config_files.ini"
    CONFIG_FILES = "CONFIG_FILES"

    def config_parser(self):
        config_parser = self._get_config_parser()
        for file_path in config_parser[self.CONFIG_FILES].items():
            config_parser.read(file_path)
        return config_parser

    def get_sections_by_file_path(self, file_path: str):
        config_parser = self._get_config_parser()
        config_parser_file_path = configparser.ConfigParser()
        config_parser_file_path.read(config_parser[self.CONFIG_FILES][file_path])
        return config_parser_file_path.sections()

    def _get_config_parser(self):
        config_parser = configparser.ConfigParser()
        config_parser.read(self.CONFIG_FILE_PATH)
        return config_parser

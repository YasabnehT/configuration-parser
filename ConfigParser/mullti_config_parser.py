import configparser
import json #Json parser
import yaml # yaml parser
import xml.etree.ElementTree as ET
import os
from pathlib import Path


"""
Basic concepts
- Polymorphism: Using a common interface to handle different configuration file formats.
- Encapsulation: Encapsulating parsing logic within a class to improve modularity and reusability.
- Error Handling: Robust error handling for various scenarios, such as missing files, unsupported formats, and malformed data.
"""
class ConfigParser:
    def __init__(self, file_path):
        self.file_path = file_path
        self.file_extension = Path(file_path).suffix.lower()
        self.config_data = None
    
    def parse(self):
        if self.file_extension =='.ini':
            self.config_data = self._parse_ini()
        elif self.file_extension =='.json':
            self.config_data = self._parse_json()
        elif self.file_extension == '.yaml':
            self.config_data = self._parse_yaml()
        elif self.file_extension == '.xml':
            self.config_data = self._parse_xml()
        else:
            raise ValueError(f'Unsupported file format: {self.file_extension}')
        
    def _parse_ini(self):
        config = configparser.ConfigParser()
        config.read(self.file_path)
        return {section: dict(config.items(section)) for  section in config.sections()}

    def _parse_json(self):
        with open(self.file_path,'r') as f:
            return json.load(f)


    def _parse_yaml(self):
        with open(self.file_path,'r') as f:
            return yaml.safe_load(f)


    def _parse_xml(self):
        tree = ET.parse(self.file_path)
        root = tree.getroot()
        return self._parse_xml_recursive(root)

    def _parse_xml_recursive(self, element):
        data = {}
        for child in element:
            if len(child):
                data[child.tag] = self._parse_xml_recursive(child)
            else:
                data[child.tag] = child.text
        return data

    def get_value(self, key_path):
        keys = key_path.split('.')
        value = self.config_data
        for key in keys:
            value  = value.get(key)
            if value is None:
                raise KeyError(f'Key {key_path} not found in configuration')
        return value

    def update_value(self, key_path, value):
        keys = key_path.split('.')
        data = self.config_data
        for key in keys[:-1]:
            data = data.get(key)
            if data is None:
                raise KeyError(f'Key {key_path} not found')
        data[keys[-1]] = value

    def save(self):
        if self.file_extension == '.ini':
            self._save_ini()
        elif self.file_extension == '.json':
            self._save_json()
        elif self.file_extension == '.yaml':
            self._save_yaml()
        elif self.file_extension == '.xml':
            self._save_xml()

        else:
            raise ValueError(f'Unsupported file format: {self.file_extension}')
        
    def _save_ini(self):
        config = configparser.ConfigParser()
        for section, options in self.config_data.items():
            config[section] = options
        with open(self.file_path, 'w') as configfile:
            config.write(configfile)

    def _save_json(self):
        with open(self.file_path, 'w') as f:
            json.dump(self.config_data, f, indent=4)

    def _save_yaml(self):
        with open(self.file_path, 'w') as f:
            yaml.dump(self.config_data, f)

    def _save_xml(self):
        root = self._dict_to_xml(self.config_data)
        tree = ET.ElementTree(root)
        tree.write(self.file_path, encoding='utf-8', xml_declaration=True)

    def _dict_to_xml(self, data, tag='root'):
        element = ET.Element(tag)
        for key, val in data.items():
            if isinstance(val, dict):
                child = self._dict_to_xml(val, tag=key)
                element.append(child)
            else: child = ET.Element(key)
            child.text = str(val)
            element.append(child)
        return element


#Example
def main():
    #paths of config files
    ini_file = '/workspaces/configuration-parser/ConfigParser/config_files/config.ini'
    json_file = '/workspaces/configuration-parser/ConfigParser/config_files/config.json'
    yaml_file = '/workspaces/configuration-parser/ConfigParser/config_files/config.yaml'
    xml_file = '/workspaces/configuration-parser/ConfigParser/config_files/config.xml'

    #crete parser instances
    for file in [ini_file, json_file, yaml_file,xml_file]:
        if os.path.exists(file):
            parser = ConfigParser(file)
            parser.parse()
            print(f'Configuration for {file}: ')
            print(parser.config_data)

            #get value
            try:
                db_host = parser.get_value('Database.host')
                print(f'Database Host: {db_host}')
            except KeyError as e:
                print(e)
            
            #Update a value and save the file
            parser.update_value("Database.host",'new_host_value')
            parser.save()
            print(f'Update and save config for {file}')


if __name__ == "__main__":
    main()



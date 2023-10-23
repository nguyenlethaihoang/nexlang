# settings.py

import json


def load_comments_from_json(filename="data/comments.json"):
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)


def load_languages_from_json(filename="data/languages.json"):
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)


def load_config_from_json(filename="data/config.json"):
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)


def load_settings_from_template(filename="settings_template.txt"):
    settings = {}
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            key, value = line.strip().split(' = ')
            # Chuyển đổi giá trị sang kiểu dữ liệu thích hợp
            if value.isdigit():
                value = int(value)
            elif value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            settings[key] = value
    return settings

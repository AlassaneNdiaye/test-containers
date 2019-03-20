import yaml


def parse_yaml_file(path):
    with open(path, "r") as f:
        yaml_content = yaml.full_load(f)
    return yaml_content


def nested_get(dictionary, *keys):
    value = dictionary
    for key in keys:
        try:
            value = value[key]
        except KeyError:
            value = None
    return value

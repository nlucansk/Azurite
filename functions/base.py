from rich import print
from rich.panel import Panel
from cdktf import Token


def print_info(_ns):
    print(Panel.fit(">>> {} <<<".format(_ns)))


def get_null_value():
    return Token.as_string(Token.null_value())


def generate_resource_tags(_tags):
    tags = {}
    if _tags is None:
        return None
    for key, value in _tags.items():
        tags[key] = value
    return tags
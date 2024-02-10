import pathlib
import tomli

import log


def get_project_root_path():
    project_root_path = pathlib.Path(__file__).resolve().parent
    log.debug(msg=f"TOML configuration file path: {project_root_path}")
    return project_root_path


def get_config_file_path():
    return get_project_root_path() / "config" / "config.toml"


with open(get_config_file_path(), mode="rb") as configuration_file:
    settings = tomli.load(configuration_file)


def get_str(section: str, item: str, attribute: str) -> str:
    if section not in settings:
        log.error(f"missing section {section} in TOML configuration file.")
    section_dict = settings[section]
    if item not in section_dict:
        log.error(f"missing item {item} in section {section} of the TOML configuration file.")
    item_dict = section_dict[item]
    if attribute not in item_dict:
        log.error(f"missing attribute {attribute} on item {item} in section {section} of the TOML configuration file.")
    attribute = item_dict[attribute]
    return attribute

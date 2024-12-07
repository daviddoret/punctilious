from __future__ import annotations
import io
import yaml
import importlib.resources


def get_yaml_from_package(path: str, resource: str) -> dict:
    """Import a yaml file from a package.

    This method is called when processing imports with `source_type: python_package_resources`.

    :param path: A python importlib.resources.files folder, e.g. `data.operators`.
    :param resource: A yaml filename, e.g. `operators_1_representations.yaml`.
    :return:
    """
    package_path = importlib.resources.files(path).joinpath(resource)
    with importlib.resources.as_file(package_path) as file_path:
        with open(file_path, 'r') as file:
            file: io.TextIOBase
            d: dict = yaml.safe_load(file)
            return d

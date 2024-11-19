import importlib.resources

template_res = importlib.resources.files("data.connectors").joinpath("operators_1.yaml")
with importlib.resources.as_file(template_res) as template_file:
    t = template_file.read_text()
    print(t)

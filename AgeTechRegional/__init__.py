import importlib

for _module_name in ("catalog", "config", "pipeline"):
    _module = importlib.import_module(_module_name)
    for _name in dir(_module):
        if _name.startswith("__"):
            continue
        globals()[_name] = getattr(_module, _name)

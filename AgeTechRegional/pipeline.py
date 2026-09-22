import importlib
_module = importlib.import_module("pipeline")
for _name in dir(_module):
    if _name.startswith("__"):
        continue
    globals()[_name] = getattr(_module, _name)

import importlib


def get_object_of(fully_qualified_name):
    module_name, class_name = fully_qualified_name.rsplit(".", 1)
    cls = getattr(importlib.import_module(module_name), class_name)
    return cls()


def get_class_of(fully_qualified_name):
    module_name, class_name = fully_qualified_name.rsplit(".", 1)
    return getattr(importlib.import_module(module_name), class_name)

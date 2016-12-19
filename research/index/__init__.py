import importlib
import json
import os.path

import research.coding.varbyte


def raise_property_not_found(prop):
    raise KeyError("property '%s' not found" % prop)


class Metadata:
    f_coding = "coding"
    f_path = "paths"
    f_type = "type"
    f_dir = "dir"
    f_name = "name"

    def __init__(self, properties):
        """
        :param properties: dict-like JSON object with properties
        """

        if Metadata.f_type not in properties:
            raise_property_not_found(Metadata.f_type)
        else:
            self.type = properties[Metadata.f_type]

        if Metadata.f_name not in properties:
            raise_property_not_found(Metadata.f_name)
        else:
            self.name = properties[Metadata.f_name]

        if Metadata.f_dir not in properties:
            raise_property_not_found(Metadata.f_dir)
        else:
            self.dir = properties[Metadata.f_dir]

        if Metadata.f_coding not in properties:
            self.coder_factory = research.coding.varbyte.Factory
        else:
            module_name, class_name = properties[Metadata.f_coding].rsplit(".", 1)
            factory_class = getattr(importlib.import_module(module_name), class_name)
            self.coder_factory = factory_class()

        if Metadata.f_path not in properties:
            raise_property_not_found(Metadata.f_path)
        else:
            self.paths = properties[Metadata.f_path]


class Index:
    def __init__(self, properties):
        self.metadata = IndexMetadata(properties)

    # def writer(self):
#


class IndexWriter:

    def __init__(self, metadata):
        self.counts_stream = open(metadata.counts_path, 'bw')
        self.counts_encoder = metadata.coder_factory.encoder()

    def close(self):
        self.counts_stream.close()


class IndexMetadata(Metadata):

    def __init__(self, properties):
        super(IndexMetadata, self).__init__(properties)
        assert properties[Metadata.f_type] == "{0}.{1}".format(Index.__module__, Index.__name__)

    def counts_path(self):
        os.path.join(self.dir, ".counts")

    def counts_offsets_path(self):
        os.path.join(self.dir, ".counts#offsets")


class IndexFactory:

    @staticmethod
    def from_path(path):
        with open(path) as file:
            properties = json.loads(file.read())
            properties["dir"] = path
            return IndexFactory.from_json(properties)

    @staticmethod
    def from_json(properties):
        if Metadata.f_type not in properties:
            raise_property_not_found(Metadata.f_type)
        module_name, class_name = properties[Metadata.f_type].rsplit(".", 1)
        index_class = getattr(importlib.import_module(module_name), class_name)
        return index_class(properties)

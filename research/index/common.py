import json
import os.path
import struct

import typing.io

import research.coding.varbyte
import research.utils


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
        # assert properties[Metadata.f_type] == "{0}.{1}".format(Index.__module__, Index.__name__)

    def docs_path(self):
        return os.path.join(self.dir, self.name + ".docs")

    def docs_offsets_path(self):
        return os.path.join(self.dir, self.name + ".docs#offsets")

    def counts_path(self):
        return os.path.join(self.dir, self.name + ".counts")

    def counts_offsets_path(self):
        return os.path.join(self.dir, self.name + ".counts#offsets")

    def frequencies_path(self):
        return os.path.join(self.dir, self.name + ".frequencies")

    def terms_path(self):
        return os.path.join(self.dir, self.name + ".terms")


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
        return research.utils.get_class_of(properties[Metadata.f_type])(properties)


def write_header(header, stream: typing.io.BinaryIO) -> int:
    """
    Write a header object to a byte stream.
    :param header: a JSON object describing properties of the file, e.g., encoding
    :param stream: a byte stream to write the header to
    :return: the number of bytes written
    """
    encoded = json.dumps(header).encode()
    encoded_len = len(encoded)
    stream.write(encoded_len.to_bytes(4, byteorder='big'))
    stream.write(encoded)
    return encoded_len + 4


def read_header(stream: typing.io.BinaryIO):
    """
    Read a header object from a byte stream.
    :param stream: a byte stream to read from
    :return: (<a JSON object describing properties of the file, e.g., encoding>,
              <the number of bytes written>)
    """
    length = struct.unpack('>i', stream.read(4))[0]
    return json.loads(stream.read(length).decode()), length + 4


def load_numbers(file_path: str) -> [int]:
    """
    Load numbers from a file to a list.
    :param file_path: the path to an offset file
    :return: a list of offsets
    """
    with open(file_path, 'br') as f:
        header, l = read_header(f)
        assert Metadata.f_coding in header, \
            "File {0} metadata does not contain encoding information".format(file_path)
        assert 'count' in header, \
            "File {0} metadata does not contain the count".format(file_path)
        decoder = research.utils.get_class_of(header[Metadata.f_coding]).Decoder(f)
        return [decoder.decode() for i in range(header['count'])]


def getp(header, property: str):
    assert property in header, "could not found property {0} in the header".format(property)
    return header[property]


def resolve_decoder(header, stream):
    return research.utils.get_class_of(getp(header, Metadata.f_coding)).Decoder(stream)

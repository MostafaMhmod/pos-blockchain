import json

import jsonpickle
from cryptography.hazmat.primitives import hashes
from eth_utils import keccak


class BlockchainUtils:
    @staticmethod
    def hash(data):
        data_string = json.dumps(data)
        data_bytes = data_string.encode("utf-8")

        return keccak(data_bytes)

    @staticmethod
    def encode(obj):
        return jsonpickle.encode(obj, unpicklable=True)

    @staticmethod
    def decode(encoded_obj):
        # CAUTION: Never deserialize data that you can not 100% trust
        return jsonpickle.decode(encoded_obj)  # nosec

import json
from typing import Any, Dict

import jsonpickle
from cryptography.hazmat.primitives import hashes
from eth_utils import keccak


class BlockchainUtils:
    """Utility functions for the blockchain system."""

    @staticmethod
    def hash(data: Dict[str, Any]) -> bytes:
        """
        Hash data using keccak.
        """
        data_string = json.dumps(data, sort_keys=True)
        data_bytes = data_string.encode("utf-8")
        return keccak(data_bytes)

    @staticmethod
    def encode(obj: Any) -> str:
        """
        Encode an object using jsonpickle.
        
        """
        return jsonpickle.encode(obj, unpicklable=True)

    @staticmethod
    def decode(encoded_obj: str) -> Any:
        """
        Decode an object using jsonpickle.
        
        """
        return jsonpickle.decode(encoded_obj)
import copy
import time
import uuid
from typing import Dict, Any


class Transaction:
    """Represents a transaction in the blockchain."""

    def __init__(self, sender_public_key: str, receiver_public_key: str, amount: float, type: str) -> None:
        """
        Initialize a new transaction.
        """
        self.sender_public_key = sender_public_key
        self.receiver_public_key = receiver_public_key
        self.amount = amount
        self.type = type
        self.id = uuid.uuid1().hex
        self.timestamp = time.time()
        self.signature = ""

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the transaction to a dictionary representation.
        
        """
        return self.__dict__

    def sign(self, signature: str) -> None:
        """
        Sign the transaction with the given signature.
        
        """
        self.signature = signature

    def payload(self) -> Dict[str, Any]:
        """
        Get the payload of the transaction (without signature).
        
        """
        dict_representation = copy.deepcopy(self.to_dict())
        dict_representation["signature"] = ""
        return dict_representation

    def equals(self, transaction: 'Transaction') -> bool:
        """
        Check if this transaction equals another transaction.
        
        """
        if self.id == transaction.id:
            return True
        return False
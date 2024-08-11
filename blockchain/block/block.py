import copy
import time
from typing import List, Any, Dict

from ..transaction import Transaction


class Block:
    """Represents a block in the blockchain."""

    def __init__(self, transactions: List[Transaction], last_hash: str, forger: str, block_height: int) -> None:
        """
        Initialize a new block.
        
        Args:
            transactions: List of transactions in the block
            last_hash: Hash of the previous block
            forger: Public key of the forger
            block_height: Height of the block in the chain
        """
        self.transactions = transactions
        self.last_hash = last_hash
        self.forger = forger
        self.block_height = block_height
        self.timestamp = time.time()
        self.signature = ""

    @staticmethod
    def genesis() -> 'Block':
        """
        Create the genesis block.
        """
        genesis_block = Block([], "genesis_hash", "genesis", 0)
        genesis_block.timestamp = 0
        return genesis_block

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the block to a dictionary representation.
        
        """
        data = copy.deepcopy(self.__dict__)
        transactions_readable = []
        for transaction in data["transactions"]:
            transactions_readable.append(transaction.to_dict())
        data["transactions"] = transactions_readable
        return data

    def payload(self) -> Dict[str, Any]:
        """
        Get the payload of the block (without signature).
        
        """
        dict_representation = copy.deepcopy(self.to_dict())
        dict_representation["signature"] = ""
        return dict_representation

    def sign(self, signature: str) -> None:
        """
        Sign the block with the given signature.
        
        """
        self.signature = signature
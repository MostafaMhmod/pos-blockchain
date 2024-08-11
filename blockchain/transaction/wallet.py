import os
from typing import Any, Dict

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa, utils

from ..block.block import Block
from .transaction import Transaction
from ..utils.helpers import BlockchainUtils

from eth_keys import keys
from eth_utils import decode_hex


class Wallet:
    """Represents a wallet in the blockchain system."""

    def __init__(self) -> None:
        """Initialize a new wallet with a random private key."""
        self.key_pair = keys.PrivateKey(os.urandom(32))

    def from_key(self, file_path: str) -> None:
        """
        Load a private key from a file.
        
        """
        with open(file_path, "r") as key_file:
            key_hex = key_file.read().strip()
            self.key_pair = keys.PrivateKey(decode_hex(key_hex))

    def sign(self, data: Dict[str, Any]) -> str:
        """
        Sign data with the wallet's private key.
        
        """
        data_hash = BlockchainUtils.hash(data)
        signature = self.key_pair.sign_msg(data_hash)
        return str(signature)

    @staticmethod
    def signature_valid(data: Dict[str, Any], signature: str, public_key_string: str) -> bool:
        """
        Verify a signature.
        
        """
        if public_key_string == 'COINBASE':
            return True

        signature_bytes = decode_hex(signature)
        signature_obj = keys.Signature(signature_bytes)

        data_hash = BlockchainUtils.hash(data)
        public_key = keys.PublicKey(decode_hex(public_key_string))

        is_valid = public_key.verify_msg(data_hash, signature_obj)
        return is_valid

    def public_key_string(self) -> str:
        """
        Get the public key as a string.
        
        """
        public_key = self.key_pair.public_key
        return public_key.to_hex()

    def create_coinbase_transaction(self, receiver: str, amount: float, type: str) -> Transaction:
        """
        Create a coinbase transaction.
        
        """
        transaction = Transaction("COINBASE", receiver, amount, type)
        signature = self.sign(transaction.payload())
        transaction.sign(signature)
        return transaction
    
    def create_transaction(self, receiver: str, amount: float, type: str) -> Transaction:
        """
        Create a transaction.
        
        """
        transaction = Transaction(self.public_key_string(), receiver, amount, type)
        signature = self.sign(transaction.payload())
        transaction.sign(signature)
        return transaction

    def create_block(self, transactions: list, last_hash: str, block_height: int) -> Block:
        """
        Create a block.
        
        """
        block = Block(transactions, last_hash, self.public_key_string(), block_height)
        signature = self.sign(block.payload())
        block.sign(signature)
        return block
import logging, os
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa, utils

from blockchain.block import Block
from blockchain.transaction.transaction import Transaction
from blockchain.utils.helpers import BlockchainUtils

from eth_keys import keys
from eth_utils import decode_hex


class Wallet:
    def __init__(self):
        self.key_pair = keys.PrivateKey(os.urandom(32))

    def from_key(self, file_path):
        with open(file_path, "r") as key_file:
            key_hex = key_file.read().strip()
            self.key_pair = keys.PrivateKey(decode_hex(key_hex))

    def sign(self, data):
        # if 'signature' in data:
        #     del data['signature']
        data_hash = BlockchainUtils.hash(data)
        signature = self.key_pair.sign_msg(data_hash)
        return str(signature)

    @staticmethod
    def signature_valid(data, signature, public_key_string):
        if public_key_string == 'COINBASE':
            return True

        signature_bytes = decode_hex(signature)
        signature = keys.Signature(signature_bytes)

        data_hash = BlockchainUtils.hash(data)
        public_key = keys.PublicKey(decode_hex(public_key_string))

        is_valid = public_key.verify_msg(data_hash, signature)
        return is_valid

    def public_key_string(self):
        public_key = self.key_pair.public_key
        return public_key.to_hex()

    def create_coinbase_transaction(self, receiver, amount, type):
        transaction = Transaction("COINBASE", receiver, amount, type)
        signature = self.sign(transaction.payload())
        transaction.sign(signature)
        return transaction
    
    def create_transaction(self, receiver, amount, type):
        transaction = Transaction(self.public_key_string(), receiver, amount, type)
        signature = self.sign(transaction.payload())
        transaction.sign(signature)
        return transaction

    def create_block(self, transactions, last_hash, block_height):
        block = Block(transactions, last_hash, self.public_key_string(), block_height)
        signature = self.sign(block.payload())
        block.sign(signature)
        return block

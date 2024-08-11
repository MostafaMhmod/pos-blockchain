import time
import copy
import threading
from typing import List, Any, Optional

from api.main import NodeAPI
from ..blockchain import Blockchain
from ..p2p.p2p_communication import SocketCommunication, Message
from ..transaction.transaction_pool import TransactionPool
from ..transaction.transaction import Transaction
from ..transaction.wallet import Wallet
from ..utils.helpers import BlockchainUtils
from ..utils.logger import logger


class Node:
    def __init__(self, ip, port, api_port, key=None):
        """Initialize a new Node.
        Args:
            ip: The IP address for the node
            port: The port for P2P communication
            api_port: The port for the REST API
            key: Optional key for the wallet
        """
        self.p2p = None
        self.ip = ip
        self.port = port
        self.api_port = api_port
        self.transaction_pool = TransactionPool()
        self.wallet = Wallet()
        self.blockchain = Blockchain()
        if key:
            self.wallet.from_key(key)
        self.keep_running = True
        self.start_p2p()
        self.start_node_api()
        self.start_produce_block()

    def start_p2p(self):
        self.p2p = SocketCommunication(self.ip, self.port)
        self.p2p.start_socket_communication(self)

    def start_node_api(self):
        self.api = NodeAPI()
        self.api.inject_node(self)
        # Start the Uvicorn server in a separate thread
        api_thread = threading.Thread(target=self.api.start, args=(self.ip, self.api_port))
        api_thread.daemon = True
        api_thread.start()

    def start_produce_block(self):
        produce_thread = threading.Thread(target=self.run_produce_block)
        produce_thread.daemon = True
        produce_thread.start()

    def run_produce_block(self):
        while self.keep_running:
            self.produce_block()
            time.sleep(10)

    def stop(self):
        self.keep_running = False

    def produce_block(self):
        """Produce a new block if this node is the selected forger.
        
        This method checks if it's time to produce a new block based on the 
        blockchain's block time. If this node is selected as the forger, it
        creates a coinbase transaction and a new block with the transactions
        in the pool, then broadcasts it to the network.
        """
        # Test if we should start producing blocks or wait
        if not self.should_produce_block():
            return
        forger = self.blockchain.next_forger()
        if forger == self.wallet.public_key_string():
            self.create_coinbase_transaction()
            block = self.blockchain.create_block(
                self.transaction_pool.transactions, self.wallet
            )
            logger.info(
                {
                    "message": "Next forger chosen",
                    "block": block.block_height,
                    "whoami": self.p2p,
                }
            )
            self.transaction_pool.remove_from_pool(self.transaction_pool.transactions)
            message = Message(self.p2p.socket_connector, "BLOCK", block)
            self.p2p.broadcast(BlockchainUtils.encode(message))
            return

    def create_coinbase_transaction(self):
        transaction = self.wallet.create_coinbase_transaction(self.wallet.public_key_string(), self.blockchain.block_reward, 'COINBASE')
        # transaction_exists = self.transaction_pool.transaction_exists(transaction)
        # if not transaction_exists:
        #     self.transaction_pool.add_transaction(transaction)
        self.transaction_pool.add_transaction(transaction)

    def handle_transaction(self, transaction):
        """
        Validates the transaction signature and checks if it already exists
        in the transaction pool or blockchain. If valid and new, adds it to
        the transaction pool and broadcasts it to other nodes.
        """
        data = transaction.payload()
        signature = transaction.signature
        signer_public_key = transaction.sender_public_key
        signature_valid = Wallet.signature_valid(data, signature, signer_public_key)
        transaction_exists = self.transaction_pool.transaction_exists(transaction)
        transaction_in_block = self.blockchain.transaction_exists(transaction)

        if not transaction_exists and not transaction_in_block and signature_valid:
            self.transaction_pool.add_transaction(transaction)
            message = Message(self.p2p.socket_connector, "TRANSACTION", transaction)
            self.p2p.broadcast(BlockchainUtils.encode(message))

    def handle_block(self, block):
        forger = block.forger
        block_hash = block.payload()
        signature = block.signature

        block_count_valid = self.blockchain.block_count_valid(block)
        last_block_hash_valid = self.blockchain.last_block_hash_valid(block)
        forger_valid = self.blockchain.forger_valid(block)
        transactions_valid = self.blockchain.transactions_valid(block.transactions)
        signature_valid = Wallet.signature_valid(block_hash, signature, forger)

        if not block_count_valid:
            self.request_chain()

        if (
            last_block_hash_valid
            and forger_valid
            and transactions_valid
            and signature_valid
        ):
            self.blockchain.add_block(block)
            self.transaction_pool.remove_from_pool(block.transactions)

    def request_chain(self):
        message = Message(self.p2p.socket_connector, "BLOCKCHAINREQUEST", None)
        encoded_message = BlockchainUtils.encode(message)
        self.p2p.broadcast(encoded_message)

    def handle_blockchain_request(self, requesting_node):
        message = Message(self.p2p.socket_connector, "BLOCKCHAIN", self.blockchain)
        encoded_message = BlockchainUtils.encode(message)
        self.p2p.send(requesting_node, encoded_message)

    def handle_blockchain(self, blockchain):
        local_blockchain_copy = copy.deepcopy(self.blockchain)
        local_block_count = len(local_blockchain_copy.blocks)
        received_chain_block_count = len(blockchain.blocks)
        if local_block_count < received_chain_block_count:
            for block_number, block in enumerate(blockchain.blocks):
                if block_number >= local_block_count:
                    local_blockchain_copy.add_block(block)
                    self.transaction_pool.remove_from_pool(block.transactions)
            self.blockchain = local_blockchain_copy

    def forge(self):
        forger = self.blockchain.next_forger()
        if forger == self.wallet.public_key_string():
            block = self.blockchain.create_block(
                self.transaction_pool.transactions, self.wallet
            )
            logger.info(
                {
                    "message": "Next forger chosen",
                    "block": block.block_height,
                    "whoami": self.p2p,
                }
            )
            self.transaction_pool.remove_from_pool(self.transaction_pool.transactions)
            message = Message(self.p2p.socket_connector, "BLOCK", block)
            self.p2p.broadcast(BlockchainUtils.encode(message))

    def should_produce_block(self):
        last_block_timestamp = self.blockchain.blocks[-1].timestamp
        current_timestamp = time.time()
        time_since_last_block = current_timestamp - last_block_timestamp
        return time_since_last_block >= self.blockchain.block_time

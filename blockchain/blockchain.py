import logging
from typing import List, Dict, Any, Optional

from .block.block import Block
from .consensus_algorithm.proof_of_stake import ProofOfStake
from .transaction.account_model import AccountModel
from .transaction import Transaction
from .utils.helpers import BlockchainUtils
from .exceptions.exceptions import BlockValidationError, InvalidTransactionError


class Blockchain:
    """Represents the blockchain."""

    def __init__(self) -> None:
        """Initialize the blockchain with a genesis block."""
        self.blocks: List[Block] = [Block.genesis()]
        self.account_model = AccountModel()
        self.pos = ProofOfStake()
        self.block_time = 10  # block time between blocks (in seconds)
        self.block_reward = 10  # reward for forging a block
        self.peers = None

    def get_block_by_height(self, block_height: int) -> Optional[Block]:
        """
        Get a block by its height.
        
        Args:
            block_height: The height of the block to retrieve
            
        Returns:
            The block with the given height, or None if not found
        """
        for block in self.blocks:
            if block.block_height == block_height:
                return block
        return None

    def add_block(self, block: Block) -> None:
        """
        Add a block to the blockchain.
        
        Args:
            block: The block to add
        """
        self.execute_transactions(block.transactions)
        self.blocks.append(block)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the blockchain to a dictionary representation.
        
        Returns:
            Dictionary representation of the blockchain
        """
        data = {}
        blocks_readable = []
        for block in self.blocks:
            blocks_readable.append(block.to_dict())
        data["blocks"] = blocks_readable
        return data

    def block_count_valid(self, block: Block) -> bool:
        """
        Check if the block count is valid.
        
        Args:
            block: The block to validate
            
        Returns:
            True if the block count is valid, False otherwise
        """
        if self.blocks[-1].block_height == block.block_height - 1:
            return True
        return False

    def last_block_hash_valid(self, block: Block) -> bool:
        """
        Check if the last block hash is valid.
        
        Args:
            block: The block to validate
            
        Returns:
            True if the last block hash is valid, False otherwise
        """
        last_block_chain_block_hash = BlockchainUtils.hash(
            self.blocks[-1].payload()
        ).hex()
        if last_block_chain_block_hash == block.last_hash:
            return True
        return False

    def get_covered_transaction_set(self, transactions: List[Transaction]) -> List[Transaction]:
        """
        Get the set of covered transactions.
        
        Args:
            transactions: List of transactions to check
            
        Returns:
            List of covered transactions
        """
        covered_transactions = []
        for transaction in transactions:
            if self.transaction_covered(transaction):
                covered_transactions.append(transaction)
            else:
                logging.error("Transaction is not covered by sender")
        return covered_transactions

    def transaction_covered(self, transaction: Transaction) -> bool:
        """
        Check if a transaction is covered by the sender's balance.
        
        Args:
            transaction: The transaction to check
            
        Returns:
            True if the transaction is covered, False otherwise
        """
        # Assume the exchange always has the amount of tokens
        if transaction.type == "EXCHANGE" or transaction.type == "COINBASE":
            return True
        sender_balance = self.account_model.get_balance(transaction.sender_public_key)
        if sender_balance >= transaction.amount:
            return True
        return False

    def execute_transactions(self, transactions: List[Transaction]) -> None:
        """
        Execute a list of transactions.
        
        Args:
            transactions: List of transactions to execute
        """
        for transaction in transactions:
            self.execute_transaction(transaction)

    def execute_transaction(self, transaction: Transaction) -> None:
        """
        Execute a single transaction.
        
        Args:
            transaction: The transaction to execute
        """
        if transaction.type == "STAKE":
            sender = transaction.sender_public_key
            receiver = transaction.receiver_public_key
            if sender == receiver:
                amount = transaction.amount
                self.pos.update(sender, amount)
                self.account_model.update_balance(sender, -amount)
        else:
            sender = transaction.sender_public_key
            receiver = transaction.receiver_public_key
            amount = transaction.amount
            self.account_model.update_balance(sender, -amount)
            self.account_model.update_balance(receiver, amount)

    def next_forger(self) -> str:
        """
        Get the next forger.
        
        Returns:
            Public key of the next forger
        """
        last_block_hash = BlockchainUtils.hash(self.blocks[-1].payload()).hex()
        next_forger = self.pos.forger(last_block_hash)
        return next_forger

    def create_block(self, transactions_from_pool: List[Transaction], forger_wallet) -> Block:
        """
        Create a new block.
        
        Args:
            transactions_from_pool: List of transactions from the pool
            forger_wallet: Wallet of the forger
            
        Returns:
            The newly created block
        """
        covered_transactions = self.get_covered_transaction_set(transactions_from_pool)
        self.execute_transactions(covered_transactions)
        new_block = forger_wallet.create_block(
            covered_transactions,
            BlockchainUtils.hash(self.blocks[-1].payload()).hex(),
            len(self.blocks),
        )
        self.blocks.append(new_block)
        return new_block

    def transaction_exists(self, transaction: Transaction) -> bool:
        """
        Check if a transaction exists in the blockchain.
        
        Args:
            transaction: The transaction to check
            
        Returns:
            True if the transaction exists, False otherwise
        """
        for block in self.blocks:
            for block_transaction in block.transactions:
                if transaction.equals(block_transaction):
                    return True
        return False
    
    def get_transaction(self, transaction_hash: str):
        """
        Get a transaction by its hash.
        
        Args:
            transaction_hash: The hash of the transaction to retrieve
            
        Returns:
            The transaction with the given hash, or False if not found
        """
        for block in self.blocks:
            for block_transaction in block.transactions:
                if block_transaction.signature == transaction_hash:
                    return block_transaction
        return False

    def forger_valid(self, block: Block) -> bool:
        """
        Check if the forger of a block is valid.
        
        Args:
            block: The block to validate
            
        Returns:
            True if the forger is valid, False otherwise
        """
        forger_public_key = self.pos.forger(block.last_hash)
        proposed_block_forger = block.forger
        if forger_public_key == proposed_block_forger:
            return True
        return False

    def transactions_valid(self, transactions: List[Transaction]) -> bool:
        """
        Check if a list of transactions is valid.
        
        Args:
            transactions: List of transactions to validate
            
        Returns:
            True if all transactions are valid, False otherwise
        """
        covered_transactions = self.get_covered_transaction_set(transactions)
        if len(covered_transactions) == len(transactions):
            return True
        return False
    
    def get_address_balance(self, public_key):
        return self.account_model.get_balance(public_key)

    def get_address_transactions(self, public_key):
        transactions = []
        for block in self.blocks:
            for block_transaction in block.transactions:
                if block_transaction.sender_public_key == public_key or block_transaction.receiver_public_key == public_key:
                    transactions.append(block_transaction)
        return transactions

from typing import List

from .transaction import Transaction


class TransactionPool:
    """Manages the pool of pending transactions."""

    def __init__(self) -> None:
        """Initialize the transaction pool."""
        self.transactions: List[Transaction] = []

    def add_transaction(self, transaction: Transaction) -> None:
        """
        Add a transaction to the pool.
        
        """
        self.transactions.append(transaction)

    def transaction_exists(self, transaction: Transaction) -> bool:
        """
        Check if a transaction exists in the pool.
        
        """
        for pool_transaction in self.transactions:
            if pool_transaction.equals(transaction):
                return True
        return False

    def remove_from_pool(self, transactions: List[Transaction]) -> None:
        """
        Remove transactions from the pool.
        
        """
        new_pool_transactions = []
        for pool_transaction in self.transactions:
            insert = True
            for transaction in transactions:
                if pool_transaction.equals(transaction):
                    insert = False
            if insert:
                new_pool_transactions.append(pool_transaction)
        self.transactions = new_pool_transactions

    def forging_required(self) -> bool:
        """
        Check if forging is required (at least 2 transactions in pool).
        
        """
        if len(self.transactions) >= 2:
            return True
        return False
from typing import Dict, List


class AccountModel:
    """Manages account balances in the blockchain."""

    def __init__(self) -> None:
        """Initialize the account model."""
        self.accounts: List[str] = []
        self.balances: Dict[str, float] = {}

    def add_account(self, public_key_string: str) -> None:
        """
        Add an account to the model.
        
        Args:
            public_key_string: Public key of the account to add
        """
        if public_key_string not in self.accounts:
            self.accounts.append(public_key_string)
            self.balances[public_key_string] = 0

    def get_balance(self, public_key_string: str) -> float:
        """
        Get the balance of an account.
        
        Args:
            public_key_string: Public key of the account
            
        Returns:
            Balance of the account
        """
        if public_key_string not in self.accounts:
            self.add_account(public_key_string)
        return self.balances[public_key_string]

    def update_balance(self, public_key_string: str, amount: float) -> None:
        """
        Update the balance of an account.
        
        Args:
            public_key_string: Public key of the account
            amount: Amount to add to the balance (can be negative)
        """
        if public_key_string not in self.accounts:
            self.add_account(public_key_string)
        self.balances[public_key_string] += amount
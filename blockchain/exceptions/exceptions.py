
class BlockchainError(Exception):
    """Base exception for blockchain-related errors."""
    pass


class InvalidTransactionError(BlockchainError):
    """Raised when a transaction is invalid."""
    pass


class InvalidBlockError(BlockchainError):
    """Raised when a block is invalid."""
    pass


class InsufficientFundsError(BlockchainError):
    """Raised when an account has insufficient funds for a transaction."""
    pass


class InvalidSignatureError(BlockchainError):
    """Raised when a signature is invalid."""
    pass


class BlockValidationError(BlockchainError):
    """Raised when block validation fails."""
    pass
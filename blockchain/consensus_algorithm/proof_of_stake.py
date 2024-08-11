from typing import Dict, List, Optional

from ..utils.helpers import BlockchainUtils

from eth_keys import keys
from eth_utils import decode_hex

from ..utils.helpers import BlockchainUtils


class Lottery:
    """Represents a lot in the Proof of Stake lottery."""

    def __init__(self, public_key: str, iteration: int, last_block_hash: str) -> None:
        """
        Initialize a lot.
        
        """
        self.public_key = str(public_key)
        self.iteration = iteration
        self.last_block_hash = str(last_block_hash)

    def lottery_hash(self) -> str:
        """
        Generate the hash for this lot.
        
        """
        hash_data = self.public_key + self.last_block_hash
        for _ in range(self.iteration):
            hash_data = BlockchainUtils.hash(hash_data).hex()
        return hash_data

class ProofOfStake:
    """Implements the Proof of Stake consensus algorithm."""

    def __init__(self) -> None:
        """Initialize the Proof of Stake system."""
        self.stakers: Dict[str, int] = {}
        self.set_genesis_node_stake()

    def set_genesis_node_stake(self) -> None:
        """Set the initial stake for the genesis node."""
        with open("./keys/genesis_public_key.txt", "r") as key_file:
            key_hex = key_file.read().strip() 
            genesis_public_key = keys.PublicKey(decode_hex(key_hex))
        self.stakers[genesis_public_key.to_hex()] = 1

    def update(self, public_key_string: str, stake: int) -> None:
        """
        Update the stake for a public key.
        
        """
        if public_key_string in self.stakers.keys():
            self.stakers[public_key_string] += stake
        else:
            self.stakers[public_key_string] = stake

    def get(self, public_key_string: str) -> Optional[int]:
        """
        Get the stake for a public key.
        
        """
        if public_key_string in self.stakers.keys():
            return self.stakers[public_key_string]
        return None

    def validator_lotteries(self, seed: str) -> List[Lottery]:
        """
        Create lotteries for all validators based on their stake.
        
        """
        lotteries = []
        for validator in self.stakers.keys():
            for stake in range(self.get(validator)):
                lotteries.append(Lottery(validator, stake + 1, seed))
        return lotteries

    def winner_lot(self, lotteries: List[Lottery], seed: str) -> Lottery:
        """
        Determine the winning lottery.
        
        """
        winner_lot = None
        least_offset = None
        reference_hash_integer_value = int(BlockchainUtils.hash(seed).hex(), 16)
        for lottery in lotteries:
            lot_integer_value = int(lottery.lottery_hash(), 16)
            offset = abs(lot_integer_value - reference_hash_integer_value)
            if least_offset is None or offset < least_offset:
                least_offset = offset
                winner_lot = lottery
        return winner_lot

    def forger(self, last_block_hash: str) -> str:
        """
        Determine the forger for the next block.
        
        """
        lotteries = self.validator_lotteries(last_block_hash)
        winner_lot = self.winner_lot(lotteries, last_block_hash)
        return winner_lot.public_key
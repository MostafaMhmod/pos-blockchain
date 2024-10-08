from blockchain.blockchain import Blockchain
from blockchain.utils.helpers import BlockchainUtils


def test_blockchain(transaction_pool):
    wallet = transaction_pool["transaction_from_wallet"]["wallet"]
    pool = transaction_pool["pool"]

    block = wallet.create_block(pool.transactions, "last_hash", 1)

    blockchain = Blockchain()
    blockchain.add_block(block)

    blockchain_readable = blockchain.to_dict()

    assert blockchain_readable["blocks"]
    assert blockchain_readable["blocks"][0]["last_hash"] == "genesis_hash"


def test_blockchain_valid_blocks(transaction_pool):
    wallet = transaction_pool["transaction_from_wallet"]["wallet"]
    pool = transaction_pool["pool"]

    blockchain = Blockchain()

    last_hash = BlockchainUtils.hash(blockchain.blocks[-1].payload()).hex()

    block_height = blockchain.blocks[-1].block_height + 1
    block = wallet.create_block(pool.transactions, last_hash, block_height)

    assert blockchain.last_block_hash_valid(block)
    assert blockchain.block_count_valid(block)

    block_height = blockchain.blocks[-1].block_height + 10
    block = wallet.create_block(pool.transactions, last_hash, block_height)

    assert not blockchain.block_count_valid(block)

    blockchain.add_block(block)

    blockchain_readable = blockchain.to_dict()

    assert blockchain_readable["blocks"]
    assert blockchain_readable["blocks"][0]["last_hash"] == "genesis_hash"

# Proof-of-Stake Blockchain

This is a Python implementation of a Proof-of-Stake (PoS) blockchain with a P2P network, REST API, and Vue.js explorer. The project demonstrates core blockchain concepts including:

- Block creation and validation
- Proof-of-Stake consensus algorithm
- Transaction handling and wallets
- P2P networking between nodes
- REST API for blockchain interaction
- Web-based blockchain explorer

## Prerequisites

- Docker and Docker Compose
- Node.js and Yarn (for the explorer)

## Quick Start

### 1. Start the Blockchain Network

```bash
docker-compose up --build
```

This will start 4 validator nodes with the following configuration:

1. **validator_alpha** (Genesis node)
   - Node Port: 9010
   - API Port: 9050

2. **validator_beta**
   - Node Port: 9011
   - API Port: 9051

3. **validator_gamma**
   - Node Port: 9012
   - API Port: 9052

4. **validator_delta**
   - Node Port: 9013
   - API Port: 9053

### 2. Start the Blockchain Explorer

In a new terminal, navigate to the explorer directory and start the Vue.js application:

```bash
cd explorer
yarn install
yarn start
```

The explorer will be available at http://localhost:8080

### 3. Generate Sample Transactions

In a new terminal, you can generate sample transactions to test the blockchain:

```bash
python sample_transactions.py
```

This script will create various types of transactions (EXCHANGE, STAKE, TRANSFER) and post them to the first node's API.

## Project Structure

```
pos-blockchain/
├── blockchain/           # Core blockchain implementation
├── api/                 # FastAPI REST API
├── explorer/            # Vue.js blockchain explorer
├── keys/                # Key generation and storage
├── Dockerfile           # Docker image definition
├── docker-compose.yml   # Multi-node Docker setup
├── requirements.txt     # Python dependencies
├── run_node.py          # Single node runner
├── run_n_nodes.py       # Multi-node runner
└── sample_transactions.py  # Sample transaction generator
```

## API Endpoints

Each node exposes a REST API with the following endpoints:

### Blockchain
- `GET /api/v1/blockchain/` - Get the entire blockchain
- `GET /api/v1/blockchain/block/{block_height}` - Get a specific block
- `GET /api/v1/blockchain/peers/` - Get connected peers

### Transactions
- `GET /api/v1/transaction/transaction_pool/` - Get transactions in mempool
- `POST /api/v1/transaction/create/` - Create a new transaction
- `GET /api/v1/transaction/{transaction_hash}` - Get a specific transaction
- `GET /api/v1/transaction/{address}/transactions/` - Get transactions for an address
- `GET /api/v1/transaction/{address}/balance/` - Get balance for an address

### Healthcheck
- `GET /ping/` - Basic health check

## Stopping the Network

To stop the blockchain network:

```bash
docker-compose down
```
from json import JSONDecodeError

from fastapi import APIRouter, HTTPException, Request

from blockchain.utils.helpers import BlockchainUtils

router = APIRouter()


@router.get("/transaction_pool/", name="Get all transactions in pool")
async def transaction_pool(request: Request):
    node = request.app.state.node
    return node.transaction_pool.transactions


@router.post("/create/", name="Create transaction")
async def create_transaction(request: Request):
    node = request.app.state.node
    try:
        payload = await request.json()
    except JSONDecodeError:
        raise HTTPException(status_code=400, detail="Can not parse request body.")
    if "transaction" not in payload:
        raise HTTPException(status_code=400, detail="Missing transaction value")

    transaction = BlockchainUtils.decode(payload["transaction"])
    node.handle_transaction(transaction)
    return {"message": "Received transaction"}


@router.get("/{transaction_hash}", name="View transaction")
async def transaction(request: Request, transaction_hash: str):
    node = request.app.state.node
    return node.blockchain.get_transaction(transaction_hash).to_dict()


@router.get("/{address}/transactions/", name="View address transactions")
async def address_transactions(request: Request, address: str):
    node = request.app.state.node
    return node.blockchain.get_address_transactions(address)


@router.get("/{address}/balance/", name="View address balance")
async def address_balance(request: Request, address: str):
    node = request.app.state.node
    return node.blockchain.get_address_balance(address)

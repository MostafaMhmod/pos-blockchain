from fastapi import APIRouter, Request

router = APIRouter()


@router.get("/", name="View blockchain")
async def blockchain(request: Request):
    node = request.app.state.node
    return node.blockchain.to_dict()

@router.get("/block/{block_height}", name="View block")
async def block(request: Request, block_height: int):
    node = request.app.state.node
    return node.blockchain.get_block_by_height(block_height).to_dict()

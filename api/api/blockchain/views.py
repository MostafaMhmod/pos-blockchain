from fastapi import APIRouter, Request, HTTPException



# Create the blockchain router
router = APIRouter()


@router.get("/block/{block_height}", name="View block")
async def get_block(request: Request, block_height: int) -> dict:
    """
    Get a specific block by height.
    
    """
    node = request.app.state.node
    block = node.blockchain.get_block_by_height(block_height)
    if block is None:
        raise HTTPException(status_code=404, detail="Block not found")
    return block.to_dict()

@router.get("/", name="View blockchain")
async def get_blockchain(request: Request) -> dict:
    """
    Get the entire blockchain.
    
    """
    node = request.app.state.node
    return node.blockchain.to_dict()

@router.get("/peers/", name="View blockchain peers")
async def peers(request: Request):
    node = request.app.state.node
    return node.blockchain.peers

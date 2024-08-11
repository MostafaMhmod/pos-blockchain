from fastapi import APIRouter

from .blockchain import views as blockchain
from .transaction import views as transaction


# Create the main API router
router = APIRouter()

# Include sub-routers
router.include_router(blockchain.router, prefix="/blockchain", tags=["Blockchain"])
router.include_router(transaction.router, prefix="/transaction", tags=["Transactions"])
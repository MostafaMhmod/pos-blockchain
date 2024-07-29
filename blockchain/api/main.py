import uvicorn
from fastapi import FastAPI

from api.api_v1.api import router as api_router
from api.utils.log_middleware import LogMiddleware
from fastapi.middleware.cors import CORSMiddleware

# Define the allowed origins
origins = [
    "http://localhost",
    "http://localhost:8080",
]

app = FastAPI(
    docs_url="/api/v1/docs/",
    title="Blockchain API",
    description="This is an API communication interface to the node blockchain.",
    version="0.1.0",
)
app.add_middleware(LogMiddleware)
# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow specific origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

class NodeAPI:
    def __init__(self):
        global app
        self.app = app

    def start(self, ip, api_port):
        uvicorn.run(self.app, host=ip, port=api_port, log_config=None)

    def inject_node(self, injected_node):
        self.app.state.node = injected_node


@app.get("/ping/", name="Healthcheck", tags=["Healthcheck"])
async def healthcheck():
    return {"success": "pong!"}


app.include_router(api_router, prefix="/api/v1")

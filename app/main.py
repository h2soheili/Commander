from fastapi import FastAPI
import asyncio as asyncio
from starlette.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.executing import run_app
from app.utils.global_log import log_factory

logger = log_factory.get_logger(__name__)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description=" description",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    debug=True,
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.get("/")
async def running():
    return f"Server is running  on {settings.SERVER_HOST}:{settings.SERVER_PORT}{settings.API_V1_STR}"


@app.on_event("startup")
async def startup_event():
    logger.info('startup event ...')
    # loop = asyncsyncio.get_event_loop()
    """
     
     open new process for each ticker
     open new thread for each strategy
    
    """
    run_app(settings)
    # kafka_client = KafkaClient(loop, 'localhost:9092', 'topic1', 'group1')
    # kafka_client.start()
    # await asyncio.sleep(1)


@app.on_event("shutdown")
async def shutdown_event():
    logger.info('shutdown event ...')
    await asyncio.sleep(1)


if __name__ == "app.main":
    print('__________________')

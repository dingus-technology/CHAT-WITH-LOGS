"""main.py

Main FastAPI entrypoint
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, status
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from dingus.database.vector_db import get_qdrant_client
from dingus.logger import set_logging
from dingus.routers.chat import router as chat_router
from dingus.settings import APP_TITLE

set_logging()

logger = logging.getLogger(__name__)

logger.info("Creating FastAPI app")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("FastAPI startup: Setting up QdrantDatabaseClient")
    app.state.qdrant_client = get_qdrant_client()
    logger.info("FastAPI startup: QdrantDatabaseClient setup completed")
    yield


app = FastAPI(docs_url=None, redoc_url=None, title=APP_TITLE, lifespan=lifespan)
app.include_router(chat_router)
app.mount("/assets", StaticFiles(directory="/assets"), name="assets")


@app.get("/docs", include_in_schema=False)
def overridden_swagger():
    return get_swagger_ui_html(openapi_url="/openapi.json", title=APP_TITLE, swagger_favicon_url="/assets/favicon.ico")


@app.get("/health")
def health_controller():
    return {"status": "Healthy"}


@app.get("/", include_in_schema=False)
def docs_redirect_controller():
    return RedirectResponse(url="/docs", status_code=status.HTTP_303_SEE_OTHER)

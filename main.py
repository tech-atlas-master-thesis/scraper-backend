import logging
from contextlib import asynccontextmanager
from typing import Optional, Dict

from pydantic import BaseModel

from pipelineFramework import PipelineServer
from fastapi import FastAPI

from pipeline_config import PIPELINE_CONFIGS

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

pipeline_server: PipelineServer = PipelineServer()

API_BASE_URL = "/api/scraper"

class PipelineCreation(BaseModel):
    name: str
    config: Optional[Dict[str, str]] = None

@asynccontextmanager
async def lifespan(_app: FastAPI):
    # pipeline_server.start_server_async()
    yield
    # thread = pipeline_server.stop_server_async()
    # TODO: find a way to join the thread
    # thread.join()

app = FastAPI(openapi_url=API_BASE_URL + "/openapi.json", docs_url=API_BASE_URL + "/docs", redoc_url=API_BASE_URL + "/redoc", lifespan=lifespan)


@app.get(API_BASE_URL + "/hello-world/")
async def hello_world():
    return {"message": "Hello World"}

@app.get(API_BASE_URL + "/pipelines")
async def get_pipelines():
    return pipeline_server.pipelines

@app.get(API_BASE_URL + "/pipelines/{pipeline_id}")
async def get_pipeline(pipeline_id: int):
    return [pipeline for pipeline in pipeline_server.pipelines if pipeline.id == pipeline_id][0]

@app.get(API_BASE_URL + "/pipelines/{pipeline_id}")
async def get_pipeline_steps(pipeline_id: int):
    pipeline = await get_pipeline(pipeline_id)
    return [*pipeline.steps.values()]

@app.post(API_BASE_URL + "/pipelines")
async def create_pipeline(pipeline: PipelineCreation):
    config = PIPELINE_CONFIGS[pipeline.name]
    if config:
        pipeline_server.add_pipeline(config)

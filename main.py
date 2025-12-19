import uvicorn

from pipelineFramework import PipelineServer
from fastapi import FastAPI

API_BASE_URL = "/api/scraper"
app = FastAPI(openapi_url=API_BASE_URL + "/openapi.json", docs_url=API_BASE_URL + "/docs", redoc_url=API_BASE_URL + "/redoc")


@app.get(API_BASE_URL + "/")
async def root():
    return {"message": "Hello World"}


def main():
    uvicorn.run(app, host="0.0.0.0", port=8050)
    server = PipelineServer()
    server.start_server()


if __name__ == '__main__':
    main()

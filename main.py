from pipelineFramework import PipelineServer
from fastapi import FastAPI


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


def main():
    server = PipelineServer()
    server.start_server()


if __name__ == '__main__':
    main()

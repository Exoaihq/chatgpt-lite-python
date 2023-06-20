from fastapi import FastAPI, Request
from pydantic import BaseModel
from starlette.responses import Response
import os

app = FastAPI()

class Config:
    runtime = "edge"

async def handler(req: Request) -> Response:
    print(f"Handling request: {req.url}")

    try:
        azure_openai_key = False
        openai_key = False
        if "AZURE_OPENAI_API_KEY" in os.environ:
            if os.environ["AZURE_OPENAI_API_KEY"].strip() != "":
                azure_openai_key = True

        if "OPENAI_API_KEY" in os.environ:
            if os.environ["OPENAI_API_KEY"].strip() != "":
                openai_key = True

        if not azure_openai_key and not openai_key:
            return Response("OpenAI key is empty")

        return Response("Ok")

    except Exception as error:
        print(error)
        return Response("Internal Server Error", status_code=500)

@app.get("/")
async def root(request: Request):
    return await handler(request)
from fastapi import FastAPI,Request
from cacheway.config.forwarder import forward_request
import os

app = FastAPI()
url = None
method = None

@app.api_route("/{path:path}",methods=["GET"])
async def proxy(request: Request, path:str):
    url = request.url
    method = request.method
    headers = request.headers
    host = headers.get("host")
    if host == os.getenv("ORIGIN"):
        response = forward_request(url)
        return {
            "status": 200,
            "details":{
                "url":str(url),
                "method":method,
                "headers":headers
            },
            "response":response,
        }
    else:
        return {"status":421}
from fastapi import FastAPI,Request
from cacheway.config.forwarder import forward_request
import os

app = FastAPI()
url = None
method = None

cache = {}

@app.api_route("/{path:path}",methods=["GET"])
async def proxy(request: Request, path:str):
    
    url = str(request.url)
    method = request.method
    headers = request.headers
    host = headers.get("host")
    
    cache_key = f"{method} {url}"
    
    if cache_key in cache:
        return cache[cache_key]
    else:
        if host == os.getenv("ORIGIN"):
            response = forward_request(url)
            cache[cache_key] = {
                "status": response.status_code,
                "details":{
                    "url":str(url),
                    "method":method,
                    "headers":headers
                },
                "response":response.text.replace("\n",""),
            }
            return cache[cache_key]
        else:
            return {"status":421}
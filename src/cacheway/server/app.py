from fastapi import FastAPI,Request
from cacheway.config.forwarder import forward_request

app = FastAPI()
url = None
method = None

@app.api_route("/{path:path}",methods=["GET","POST","PUT","DELETE","PATCH","OPTIONS", "HEAD","CONNECT"])
async def proxy(request: Request, path:str):
    url = request.url
    method = request.method
    response = forward_request(url)
    return {
        "status": "200 ok",
        "url":str(url),
        "method":method,
        "response":response
        }

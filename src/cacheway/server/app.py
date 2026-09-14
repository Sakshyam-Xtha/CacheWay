from fastapi import FastAPI, Request
from cacheway.config.forwarder import forward_request
import os

app = FastAPI()

cache = {}

@app.api_route("/{path:path}", methods=["GET"])
async def proxy(request: Request, path: str):
    method = request.method
    origin = os.getenv("ORIGIN")

    target_url = f"https://{origin}/{path}"
    if request.url.query:
        target_url += f"?{request.url.query}"

    cache_key = f"{method} {target_url}"

    if cache_key in cache:
        return cache[cache_key]

    response = forward_request(target_url)
    cached = {
        "status": response.status_code,
        "details": {
            "url": str(request.url),
            "method": method,
            "headers": request.headers,
        },
        "response": response.text.replace("\n", ""),
    }
    cache[cache_key] = cached
    return cached
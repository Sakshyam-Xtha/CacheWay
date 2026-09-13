from fastapi import FastAPI,Request

app = FastAPI()
url = None
method = None

@app.api_route("/{path:path}",methods=["GET","POST","PUT","DELETE","PATCH"])
async def listener(request: Request, path:str):
    url = request.url
    method = request.method

    return {"status": "200 ok"}

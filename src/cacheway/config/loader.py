from dotenv import load_dotenv
import os
import uvicorn

load_dotenv()

def start_server(port,server_path):
    port = os.getenv("PORT")
    if port:
        uvicorn.run(
            "cacheway.server.app:app",
            host="127.0.0.1",
            port=int(port),
        )
    

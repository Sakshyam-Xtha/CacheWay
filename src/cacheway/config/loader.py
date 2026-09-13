from dotenv import load_dotenv
import subprocess
import os
from pathlib import Path

load_dotenv()

def start_server():
    port = os.getenv("PORT")
    origin = os.getenv("ORIGIN")
    server_path = os.getenv("SERVER_PATH")

    commands = ["fastapi","dev",server_path, "--port",port]
    subprocess.run(commands)
    
start_server()
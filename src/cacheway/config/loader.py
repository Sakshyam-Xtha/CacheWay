from dotenv import load_dotenv
import subprocess
import os
from pathlib import Path

load_dotenv()

port = os.getenv("PORT")
origin = os.getenv("ORIGIN")
server_path = os.getenv("SERVER_PATH")

if not port and not origin and not server_path:
    port = 
    commands = ["fastapi","dev",server_path, "--port",port]
    subprocess.run(commands)
    
else:
    
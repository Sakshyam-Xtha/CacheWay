from dotenv import load_dotenv
import subprocess
import os
from pathlib import Path

load_dotenv()

def start_server(port,server_path):
    commands = ["fastapi","dev",server_path, "--port",port]
    subprocess.run(commands)
    

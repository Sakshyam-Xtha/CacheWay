import typer
import argparse
import os
from dotenv import load_dotenv
from cacheway.config.helper import get_server_path,env_setter
from cacheway.config.loader import start_server

load_dotenv(override=True)

port = os.getenv("PORT")
origin = os.getenv("ORIGIN")
path = os.getenv("SERVER_PATH")

app = typer.Typer(name="cacheway")

@app.command()
def main():
    parser = argparse.ArgumentParser()
    
    parser.add_argument("--port", type=int, required=True)
    parser.add_argument("--origin", required=True)
    
    args = parser.parse_args()
    env_setter(args.port,args.origin)
    
    start_server()

if __name__ == "__main__":
    app()
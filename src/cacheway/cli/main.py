import typer
import argparse
import os
from dotenv import load_dotenv
from cacheway.config.helper import env_setter
from cacheway.config.loader import start_server

load_dotenv(override=True)

app = typer.Typer(name="cacheway")

@app.command()
def main():
    parser = argparse.ArgumentParser()
    
    parser.add_argument("--port", type=int, required=True)
    
    args = parser.parse_args()
    env_setter(args.port)
    
    port = os.getenv("PORT")
    path = os.getenv("SERVER_PATH")
    
    start_server(port,path)

if __name__ == "__main__":
    app()
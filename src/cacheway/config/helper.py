import os
from pathlib import Path
from dotenv import set_key, load_dotenv

def get_root_path():
    path = Path(__file__)
    base_path = path.resolve().parent.parent.parent.parent
    return base_path

def env_setter(port):
    env = get_root_path() / ".env"
    server_path = get_server_path()
    set_key(env,"PORT",str(port))
    set_key(env,"SERVER_PATH",str(server_path))
    load_dotenv(env, override=True)

def get_server_path():
    server_path = get_root_path() / "src" / "cacheway" / "server" / "app.py"
    return server_path

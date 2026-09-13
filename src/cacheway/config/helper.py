import os
from pathlib import Path
from dotenv import set_key

def get_root_path():
    path = Path(os.getcwd())
    base_path = path.resolve().parent.parent.parent
    return base_path

def env_setter(port,origin):
    env = ".env"
    set_key(env,"PORT",str(port))
    set_key(env,"ORIGIN",origin)
    set_key(env,"SERVER_PATH",str(get_server_path()))

def get_server_path():
    server_path = get_root_path() / "src" / "cacheway" / "server" / "app.py"
    return server_path
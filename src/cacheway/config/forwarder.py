import subprocess
import json

def forward_request(request_url)->dict:
    commands = ["curl","-s",str(request_url)]
    response = subprocess.run(commands,capture_output=True,text=True)
    return json.loads(response.stdout)
import httpx

def forward_request(request_url):
    response = httpx.get(request_url)
    return response


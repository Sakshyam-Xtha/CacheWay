# cacheway

A caching proxy built with FastAPI. It catches GET requests for a target origin URL, forwards uncached requests upstream, and serves repeat requests from an in-memory cache with a 60-second TTL.

## Installation

```bash
pip install .
```

For development:

```bash
pip install -e .[dev]
```

## Usage

Start the proxy server with a target origin:

```bash
cacheway --port 8000 --origin jsonplaceholder.typicode.com
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `--port` | Yes | Port to run the proxy server on |
| `--origin` | Yes | Upstream hostname to proxy and cache requests for |

### Example

```bash
# Proxy requests to jsonplaceholder.typicode.com on port 8000
cacheway --port 8000 --origin jsonplaceholder.typicode.com

# First request - cache miss, fetched from origin
curl http://localhost:8000/posts/1

# Second request - cache hit, served from cache
curl http://localhost:8000/posts/1
```

## How It Works

1. CLI parses `--port` and `--origin`, writes them to `.env`
2. Uvicorn starts the FastAPI server on `127.0.0.1:<port>`
3. Each GET request is checked against the in-memory cache, keyed by `method + target URL`
4. `check_ttl` purges any cached entries older than 60 seconds
5. Cache hits return the stored response immediately with `"Hit": "YES"`
6. Cache misses are forwarded to `https://{origin}/{path}` (query string preserved), cached with a timestamp, and returned with `"Hit": "NO"`
7. Only GET requests are proxied; other methods return `405`

## Response Format

```json
{
  "status": 200,
  "Hit": "YES",
  "details": {
    "url": "http://localhost:8000/posts/1",
    "method": "GET",
    "headers": {}
  },
  "response": "{\"userId\":1,\"id\":1,...}",
  "timestamp": "2025-01-01T12:00:00.000000"
}
```

## Project Structure

```
cacheway/
├── src/cacheway/
│   ├── cli/           # CLI entry point (Typer/argparse)
│   ├── config/        # Request forwarding, uvicorn server startup
│   ├── server/        # FastAPI proxy app
│   ├── cache/         # Cache module (extensible)
│   └── utils/         # Env helpers, TTL eviction
├── tests/             # Pytest suite
├── pyproject.toml
└── README.md
```

## Testing

```bash
pytest
```

## License

MIT
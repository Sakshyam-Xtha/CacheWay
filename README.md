# cacheway

A simple caching proxy server built with FastAPI. Forward requests to an origin server and cache responses in-memory for faster subsequent requests.

## Installation

```bash
pip install .
```

For development:

```bash
pip install -e .
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
| `--origin` | Yes | Origin server hostname to proxy and cache requests to |

### Example

```bash
# Proxy requests to jsonplaceholder.typicode.com on port 8000
cacheway --port 8000 --origin jsonplaceholder.typicode.com

# First request - fetched from origin
curl http://localhost:8000/posts/1

# Second request - served from cache
curl http://localhost:8000/posts/1
```

## How It Works

1. CLI parses `--port` and `--origin`, writes them to `.env`
2. FastAPI dev server starts on the specified port
3. Incoming GET requests are checked against an in-memory cache, keyed by method + target URL
4. Cache hits return the stored response immediately
5. Cache misses are forwarded to `https://{origin}/{path}`, cached, then returned
6. Only GET requests are proxied; other methods return `405`

## Project Structure

```
cacheway/
├── src/cacheway/
│   ├── cli/           # CLI entry point (Typer/argparse)
│   ├── config/        # Helpers, env setup, request forwarding
│   ├── server/        # FastAPI proxy server
│   ├── cache/         # Cache module (extensible)
│   └── utils/         # Shared utilities
├── pyproject.toml
└── README.md
```

## License

MIT

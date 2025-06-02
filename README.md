# Cursor MCP Implementation

A simple implementation of Model Context Protocol (MCP) server and client for Cursor IDE using FastMCP.

## Features

- FastMCP Server with stdio transport
- Simple prompt template ("hello-world")
- Echo tool implementation
- FastMCP Client for testing server functionality

## Setup

1. Install dependencies:
```bash
pip install -e .
```

2. Run the server:
```bash
python server.py
```

3. Run the client:
```bash
python client.py
```

## Project Structure

- `server.py`: FastMCP server implementation
- `client.py`: FastMCP client implementation
- `pyproject.toml`: Project configuration and dependencies

## Implementation Details

This project uses FastMCP, a high-level API for MCP that provides:
- Simplified server and client implementation
- Automatic type conversion and validation
- Built-in error handling
- Easy prompt and tool registration

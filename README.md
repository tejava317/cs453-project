# CS453 Automated Software Testing Final Project

## Ollama Setup

This project uses Ollama to run a local Large Language Model (LLM) for development and testing purposes. Follow the steps below to set up Ollama and connect it to the project.

### 1. Install Ollama

Download and install Ollama from the official website:
https://ollama.ai

### 2. Pull a Model

After installing Ollama, pull your desired model. For example, to use the `qwen3:14b` model, run:

```bash
ollama pull qwen3:14b
```

### 3. Run the Ollama Server

Make sure the Ollama server is running. Start it with the following command:

```bash
ollama serve
```

Once the server is running, your local LLM will be available for the project to use.


## MCPHost Setup & Configuration

To connect your local Ollama LLM to the MCP server, you need to install and configure [MCPHost](https://github.com/mark3labs/mcphost).

### 1. Install Go

Download and install Go from the official website:
https://go.dev/dl/

### 2. Install MCPHost

Install MCPHost using the following command:

```bash
go install github.com/mark3labs/mcphost@latest
```

### 3. Finish Configuration

MCPHost will automatically create a configuration file in your home directory if it doesn't exist. It looks for config files in this order:

- `.mcphost.yml` or `.mcphost.json` (preferred)
- `.mcp.yml` or `.mcp.json` (backwards compatibility)

**Config file locations by OS:**
- **Linux/macOS:** `~/.mcphost.yml`, `~/.mcphost.json`, `~/.mcp.yml`, `~/.mcp.json`
- **Windows:** `%USERPROFILE%\.mcphost.yml`, `%USERPROFILE%\.mcphost.json`, `%USERPROFILE%\.mcp.yml`, `%USERPROFILE%\.mcp.json`

You can also specify a custom location using the `--config` flag.

#### 3.1. Example STDIO MCP-server Configuration

Example `.mcphost.yml` file is provided [here](https://github.com/tejava317/cs453-project/blob/main/.mcphost.yml)

Below is an example configuration for an STDIO MCP-server:

```json
{
  "mcpServers": {
    "sqlite": {
      "command": "uvx",
      "args": [
        "mcp-server-sqlite",
        "--db-path",
        "/tmp/foo.db"
      ]
    },
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/tmp"
      ],
      "allowedTools": ["read_file", "write_file"],
      "excludedTools": ["delete_file"]
    }
  }
}
```

- Each STDIO entry requires:
  - `command`: The command to run (e.g., `uvx`, `npx`)
  - `args`: Array of arguments for the command
  - `allowedTools`: (Optional) Array of tool names to include (whitelist)
  - `excludedTools`: (Optional) Array of tool names to exclude (blacklist)

> **Note:** `allowedTools` and `excludedTools` are mutually exclusive – you can only use one per server.


### 4. Run MCPHost with Interactive Mode

Run MCPHost using following command:
```bash
mcphost -m ollama:qwen3:14b
```

For more details and advanced configuration, please refer to the official MCPHost documentation: [https://github.com/mark3labs/mcphost](https://github.com/mark3labs/mcphost)
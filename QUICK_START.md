# Quick Start Guide

This guide will help you get started with document-reader-mcp in under 5 minutes.

## Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/ifmelate/document-reader-mcp.git
cd document-reader-mcp
```

### Step 2: Set Up Environment

**Option A: Automated Setup (Recommended)**
```bash
./dev-setup.sh
```

**Option B: Manual Setup**
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Step 3: Test the Server

```bash
python -m server.main
```

You should see the server start. Press `Ctrl+C` to stop it.

## Configuration

### For Cursor IDE

1. Open Cursor Settings
2. Navigate to MCP section
3. Add this configuration:

```json
{
  "mcpServers": {
    "document-reader": {
      "command": "python3",
      "args": ["-m", "server.main"],
      "cwd": "/path/to/document-reader-mcp"
    }
  }
}
```

Replace `/path/to/document-reader-mcp` with the actual path.

### For Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or equivalent:

```json
{
  "mcpServers": {
    "document-reader": {
      "command": "python3",
      "args": ["-m", "server.main"],
      "cwd": "/path/to/document-reader-mcp"
    }
  }
}
```

## Usage Examples

Once configured, you can use these commands in your MCP client:

### Example 1: Extract PDF
```
Extract text from ~/Documents/report.pdf
```

### Example 2: Read Excel
```
Read the first 10 rows from data.xlsx
```

### Example 3: Parse CSV
```
What's in sales_data.csv?
```

### Example 4: Read JSON
```
Show me the contents of config.json
```

## Supported Formats

| Format | Extensions |
|--------|-----------|
| PDF | `.pdf` |
| Excel | `.xlsx`, `.xlsm`, `.xltx`, `.xltm` |
| Word | `.docx` |
| CSV | `.csv` |
| Text | `.txt`, `.log`, `.text` |
| JSON | `.json` |
| Markdown | `.md`, `.markdown` |

## Configuration Options

### Rate Limiting

Set the `DOC_READER_RATE_LIMIT_PER_MINUTE` environment variable:

```bash
export DOC_READER_RATE_LIMIT_PER_MINUTE=120
python -m server.main
```

Or in your MCP client configuration:

```json
{
  "mcpServers": {
    "document-reader": {
      "command": "python3",
      "args": ["-m", "server.main"],
      "cwd": "/path/to/document-reader-mcp",
      "env": {
        "DOC_READER_RATE_LIMIT_PER_MINUTE": "120"
      }
    }
  }
}
```

## Troubleshooting

### Server Won't Start
- Verify Python 3.10+ is installed: `python3 --version`
- Ensure dependencies are installed: `pip install -r requirements.txt`
- Check for port conflicts (though this uses stdio, not network)

### "Module not found" Error
- Activate the virtual environment: `source .venv/bin/activate`
- Reinstall dependencies: `pip install -r requirements.txt`

### "Unsupported file type" Error
- Check the file extension is supported (see table above)
- Verify the file exists and is readable

### Rate Limit Exceeded
- Wait 60 seconds, or
- Increase limit: `export DOC_READER_RATE_LIMIT_PER_MINUTE=120`

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check [CONTRIBUTING.md](CONTRIBUTING.md) to contribute
- Review [SECURITY.md](SECURITY.md) for security considerations
- See [RELEASE.md](RELEASE.md) for release process

## Getting Help

- **Issues**: [GitHub Issues](https://github.com/ifmelate/document-reader-mcp/issues)
- **Discussions**: [GitHub Discussions](https://github.com/ifmelate/document-reader-mcp/discussions)
- **Documentation**: [README.md](README.md)

## License

MIT License - see [LICENSE](LICENSE) file for details.


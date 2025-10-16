# Quick Start Guide

This guide will help you get started with document-reader-mcp in under 5 minutes.

## Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/ifmelate/document-reader-mcp.git
cd document-reader-mcp
```

### Step 2: Set Up Environment

#### macOS/Linux

**Option A: Automated Setup (Recommended)**
```bash
chmod +x dev-setup.sh
./dev-setup.sh
```

**Option B: Manual Setup**
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

#### Windows (Command Prompt)

**Option A: Automated Setup (Recommended)**
```cmd
dev-setup.bat
```

**Option B: Manual Setup**
```cmd
python -m venv .venv
.venv\Scripts\activate.bat
pip install -r requirements.txt
```

#### Windows (PowerShell)

**Option A: Automated Setup (Recommended)**
```powershell
.\dev-setup.ps1
```

**Option B: Manual Setup**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Step 3: Test the Server

**macOS/Linux:**
```bash
python3 -m server.main
```

**Windows:**
```cmd
python -m server.main
```

You should see the server start. Press `Ctrl+C` to stop it.

## Configuration

### For Cursor IDE

1. Open Cursor Settings
2. Navigate to MCP section
3. Add this configuration:

#### macOS/Linux Configuration

```json
{
  "mcpServers": {
    "document-reader": {
      "command": "python3",
      "args": ["-m", "server.main"],
      "cwd": "/absolute/path/to/document-reader-mcp"
    }
  }
}
```

#### Windows Configuration

```json
{
  "mcpServers": {
    "document-reader": {
      "command": "python",
      "args": ["-m", "server.main"],
      "cwd": "C:/Users/YourUsername/document-reader-mcp"
    }
  }
}
```

**Note**: Replace the path with your actual installation directory. On Windows, you can use forward slashes (`/`) or double backslashes (`\\\\`).

### For Claude Desktop

#### macOS Configuration

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

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

#### Windows Configuration

Add to `%APPDATA%\Claude\claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "document-reader": {
      "command": "python",
      "args": ["-m", "server.main"],
      "cwd": "C:/Users/YourUsername/document-reader-mcp"
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
- **macOS/Linux**: Verify Python 3.10+ is installed: `python3 --version`
- **Windows**: Verify Python 3.10+ is installed: `python --version`
- Ensure dependencies are installed: `pip install -r requirements.txt`
- Check for port conflicts (though this uses stdio, not network)

### "Module not found" Error
- **macOS/Linux**: Activate the virtual environment: `source .venv/bin/activate`
- **Windows (CMD)**: Activate the virtual environment: `.venv\Scripts\activate.bat`
- **Windows (PowerShell)**: Activate the virtual environment: `.venv\Scripts\Activate.ps1`
- Reinstall dependencies: `pip install -r requirements.txt`

### "Unsupported file type" Error
- Check the file extension is supported (see table above)
- Verify the file exists and is readable

### Rate Limit Exceeded
- Wait 60 seconds, or
- **macOS/Linux**: Increase limit: `export DOC_READER_RATE_LIMIT_PER_MINUTE=120`
- **Windows (CMD)**: Increase limit: `set DOC_READER_RATE_LIMIT_PER_MINUTE=120`
- **Windows (PowerShell)**: Increase limit: `$env:DOC_READER_RATE_LIMIT_PER_MINUTE=120`

### Windows-Specific Issues

#### PowerShell Execution Policy
If you see "cannot be loaded because running scripts is disabled":
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### Python Not Found
- Ensure Python is in your PATH
- Try using `py` instead of `python` if the installer added it: `py --version`
- Reinstall Python from [python.org](https://www.python.org/downloads/) with "Add to PATH" checked

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


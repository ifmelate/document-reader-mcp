# document-reader-mcp

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Version](https://img.shields.io/badge/version-1.0.0-green.svg)](https://github.com/ifmelate/document-reader-mcp/releases)

Universal MCP server for extracting text from various document formats. Supports streaming, page/row limits, encoding detection, and simple rate limiting.

## Supported Formats

| Format | Extensions | Dependencies | Status |
|--------|-----------|--------------|--------|
| **PDF** | `.pdf` | `pdfminer.six` | ✅ Included |
| **Excel** | `.xlsx`, `.xlsm`, `.xltx`, `.xltm` | `openpyxl` | ✅ Included |
| **Word** | `.docx` | `python-docx` | ✅ Included |
| **CSV** | `.csv` | Built-in | ✅ Always available |
| **Plain Text** | `.txt`, `.log`, `.text` | Built-in | ✅ Always available |
| **JSON** | `.json` | Built-in | ✅ Always available |
| **Markdown** | `.md`, `.markdown` | Built-in | ✅ Always available |

## Features

✅ **Multiple format support**: PDF, Excel, CSV, TXT, JSON, Markdown, DOCX  
✅ **Streaming API**: Memory-efficient processing of large files  
✅ **Smart encoding detection**: Handles UTF-8, Latin-1, CP1252, ISO-8859-1  
✅ **Rate limiting**: Process-wide rate limiting (configurable)  
✅ **Modular design**: Easy to extend with new formats  
✅ **Minimal dependencies**: Most formats use Python stdlib only

## Installation

### Option 1: Install from GitHub (Recommended)

```bash
# Clone the repository
git clone https://github.com/ifmelate/document-reader-mcp.git
cd document-reader-mcp

# Create virtual environment and install dependencies
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Option 2: Direct Install with pip

```bash
pip install git+https://github.com/ifmelate/document-reader-mcp.git
```

### Running the Server

After installation, start the MCP server:

```bash
python -m server.main
```

The server runs over stdio for integration with MCP-compatible clients.

## Configuration in Cursor (or other MCP clients)

### For Cursor IDE

Add this configuration to your Cursor MCP settings (usually in `~/.cursor/mcp.json` or via Settings → MCP):

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

Replace `/absolute/path/to/document-reader-mcp` with the actual path where you cloned the repository.

### For Claude Desktop or other MCP clients

Add similar configuration to your client's MCP settings file, adjusting the path accordingly.

## Available Tools

Once configured, you can use these tools:

### Tool: `extract_text_from_file`

Extract complete text from a document file.

**Parameters:**
- `path` (string, required): Absolute or relative path to the document
- `max_pages` (int, optional): For PDFs, parse only the first N pages
- `max_rows` (int, optional): For CSV/Excel, parse only N data rows

**Returns:** Extracted text as string

**Supported formats:** `.pdf`, `.xlsx`, `.xlsm`, `.csv`, `.txt`, `.json`, `.md`, `.docx`

**Note:** For large files, use `extract_text_from_file_stream` instead to avoid memory issues.

### Tool: `extract_text_from_file_stream`

Stream text chunks from a document (memory-efficient for large files).

**Parameters:**
- `path` (string, required): Absolute or relative path to the document
- `max_pages` (int, optional): For PDFs, page cap
- `max_rows` (int, optional): For CSV/Excel, row cap
- `chunk_size` (int, optional): Characters per chunk (default: 4096, min: 512)

**Yields:** Text chunks as strings

**Supported formats:** All formats from `extract_text_from_file`

## Usage Examples

### In Cursor Chat:

```
Extract text from ~/Downloads/report.pdf and summarize the findings
```

```
Read the CSV file data.csv and show me the first 10 rows
```

```
What's in the JSON file config.json?
```

### Programmatic Usage:

```python
# Via MCP client
result = await client.call_tool("extract_text_from_file", {
    "path": "/path/to/document.pdf",
    "max_pages": 5
})

# Streaming
async for chunk in client.stream_tool("extract_text_from_file_stream", {
    "path": "/path/to/large_file.csv",
    "chunk_size": 8192
}):
    print(chunk)
```

## Configuration

### Environment Variables

- `DOC_READER_RATE_LIMIT_PER_MINUTE`: Maximum tool calls per minute (default: 60)

Example:
```bash
export DOC_READER_RATE_LIMIT_PER_MINUTE=120
python -m server.main
```

## Technical Details

### File Size Limits
- Maximum file size: **100 MB**
- Files larger than this will be rejected with an error

### Encoding Detection
Text-based formats (CSV, TXT, JSON, Markdown) automatically try multiple encodings:
- UTF-8
- Latin-1 (ISO-8859-1)
- Windows-1252 (CP1252)

### Dependencies by Format

| Format | Library | Type |
|--------|---------|------|
| PDF | `pdfminer.six` | Included |
| Excel | `openpyxl` | Included |
| Word | `python-docx` | Included |
| CSV | `csv` (stdlib) | Built-in |
| TXT | File I/O (stdlib) | Built-in |
| JSON | `json` (stdlib) | Built-in |
| Markdown | File I/O (stdlib) | Built-in |

## Security Considerations

⚠️ **Important**: This server reads local files from the filesystem.

- **Do NOT expose this server to untrusted networks**
- Only use in trusted MCP client environments (e.g., Cursor IDE)
- Rate limiting is per-process, not per-user
- No authentication is built-in
- File paths are expanded with `os.path.expanduser()` (supports `~`)

## Troubleshooting

### "Unsupported file type" error
- Check that the file extension matches one of the supported formats
- Supported: `.pdf`, `.xlsx`, `.xlsm`, `.xltx`, `.xltm`, `.docx`, `.csv`, `.txt`, `.log`, `.json`, `.md`, `.markdown`

### "Failed to decode" error
- The file may use an unsupported text encoding
- Try converting the file to UTF-8 encoding first
- This typically affects CSV, TXT, JSON, and Markdown files

### Rate limit exceeded
- Increase the `DOC_READER_RATE_LIMIT_PER_MINUTE` environment variable
- Or wait 60 seconds for the rate limit window to reset

### Missing dependency errors
- If you see "X is not installed" errors, reinstall dependencies: `pip install -r requirements.txt`

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on:

- Setting up your development environment
- Code style and commit conventions
- Adding support for new file formats
- Submitting pull requests

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- **Issues**: [GitHub Issues](https://github.com/ifmelate/document-reader-mcp/issues)
- **Discussions**: [GitHub Discussions](https://github.com/ifmelate/document-reader-mcp/discussions)

## Version

Current version: **1.0.0**

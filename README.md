# document-reader-mcp

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Version](https://img.shields.io/badge/version-1.0.0-green.svg)](https://github.com/ifmelate/document-reader-mcp/releases)
[![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Linux%20%7C%20Windows-lightgrey.svg)](https://github.com/ifmelate/document-reader-mcp)

Universal MCP server for extracting text from various document formats. Supports streaming, page/row limits, encoding detection, and simple rate limiting.

**Cross-platform compatible**: Works seamlessly on macOS, Linux, and Windows with identical functionality.

## Supported Formats

| Format | Extensions | Dependencies | Status |
|--------|-----------|--------------|--------|
| **PDF** | `.pdf` | `pdfminer.six`, `pymupdf` | ✅ Included (text + images) |
| **Excel** | `.xlsx`, `.xlsm`, `.xltx`, `.xltm` | `openpyxl` | ✅ Included |
| **Word** | `.docx` | `python-docx` | ✅ Included |
| **CSV** | `.csv` | Built-in | ✅ Always available |
| **Plain Text** | `.txt`, `.log`, `.text` | Built-in | ✅ Always available |
| **JSON** | `.json` | Built-in | ✅ Always available |
| **Markdown** | `.md`, `.markdown` | Built-in | ✅ Always available |

## Features

✅ **Cross-platform**: Works on macOS, Linux, and Windows  
✅ **Multiple format support**: PDF, Excel, CSV, TXT, JSON, Markdown, DOCX, PowerPoint, HTML  
✅ **Markdown conversion**: Convert documents to Markdown with automatic image extraction  
✅ **PDF image extraction**: Automatically extracts and embeds images from PDFs at appropriate page positions  
✅ **Streaming API**: Memory-efficient processing of large files  
✅ **Smart encoding detection**: Handles UTF-8, Latin-1, CP1252, ISO-8859-1  
✅ **Context-aware limits**: Automatic truncation to prevent AI context overflow  
✅ **Rate limiting**: Process-wide rate limiting (configurable)  
✅ **Docker support**: Run in isolated container with non-root user  
✅ **Modular design**: Easy to extend with new formats  
✅ **Minimal dependencies**: Most formats use Python stdlib only

## Installation

### Option 1: Install from GitHub (Recommended)

#### macOS/Linux

```bash
# Clone the repository
git clone https://github.com/ifmelate/document-reader-mcp.git
cd document-reader-mcp

# Create virtual environment and install dependencies
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

#### Windows (Command Prompt)

```cmd
# Clone the repository
git clone https://github.com/ifmelate/document-reader-mcp.git
cd document-reader-mcp

# Create virtual environment and install dependencies
python -m venv .venv
.venv\Scripts\activate.bat
pip install -r requirements.txt
```

#### Windows (PowerShell)

```powershell
# Clone the repository
git clone https://github.com/ifmelate/document-reader-mcp.git
cd document-reader-mcp

# Create virtual environment and install dependencies
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**Note for Windows PowerShell users**: If you encounter an execution policy error, run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### Quick Setup Scripts

For convenience, you can use the provided setup scripts:

**macOS/Linux:**
```bash
chmod +x dev-setup.sh
./dev-setup.sh
```

**Windows (Command Prompt):**
```cmd
dev-setup.bat
```

**Windows (PowerShell):**
```powershell
.\dev-setup.ps1
```

These scripts will create the virtual environment, install dependencies, and set up the development environment automatically.

### Option 2: Direct Install with pip

```bash
pip install git+https://github.com/ifmelate/document-reader-mcp.git
```

### Option 3: Docker

```bash
# Clone the repository
git clone https://github.com/ifmelate/document-reader-mcp.git
cd document-reader-mcp

# Build the Docker image
docker build -t document-reader-mcp:latest .
```

See [Docker Configuration](#docker-configuration) below for MCP client setup.

### Running the Server

After installation, start the MCP server:

```bash
python -m server.main
```

The server runs over stdio for integration with MCP-compatible clients.

## Configuration in Cursor (or other MCP clients)

### For Cursor IDE

Add this configuration to your Cursor MCP settings:
- **macOS/Linux**: `~/.cursor/mcp.json`
- **Windows**: `%APPDATA%\Cursor\User\globalStorage\mcp.json` or via Settings → MCP

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
      "cwd": "C:\\Users\\YourUsername\\document-reader-mcp"
    }
  }
}
```

**Important for Windows users**:
- Use double backslashes (`\\`) in JSON paths, or use forward slashes (`/`) which also work on Windows
- Replace `YourUsername` with your actual Windows username
- Ensure the `python` command points to your Python 3.10+ installation (check with `python --version`)

### For Claude Desktop or other MCP clients

Add similar configuration to your client's MCP settings file, adjusting the path accordingly.

### Docker Configuration

To use the Docker version with MCP clients:

```json
{
  "mcpServers": {
    "document-reader": {
      "command": "docker",
      "args": [
        "run",
        "--rm",
        "-i",
        "-v", "/absolute/path/to/documents:/documents:ro",
        "document-reader-mcp:latest"
      ]
    }
  }
}
```

**Important notes:**
- Replace `/absolute/path/to/documents` with the directory containing files you want to process
- The `-v` flag mounts your documents directory as `/documents` in the container (read-only)
- Use `-i` for interactive mode (required for stdio communication)
- Use `--rm` to automatically remove the container after it stops
- File paths in MCP tool calls should use `/documents/filename.pdf` format

**Multiple volume mounts:**

If you need to access files from multiple directories:

```json
{
  "mcpServers": {
    "document-reader": {
      "command": "docker",
      "args": [
        "run",
        "--rm",
        "-i",
        "-v", "/Users/you/Documents:/documents:ro",
        "-v", "/Users/you/Downloads:/downloads:ro",
        "document-reader-mcp:latest"
      ]
    }
  }
}
```

**Custom rate limiting:**

```json
{
  "mcpServers": {
    "document-reader": {
      "command": "docker",
      "args": [
        "run",
        "--rm",
        "-i",
        "-e", "DOC_READER_RATE_LIMIT_PER_MINUTE=120",
        "-v", "/absolute/path/to/documents:/documents:ro",
        "document-reader-mcp:latest"
      ]
    }
  }
}
```

**Security considerations for Docker:**
- The container runs as non-root user (UID 1000)
- Volumes are mounted read-only (`:ro`) for safety
- No network ports are exposed
- Container has minimal attack surface

## Available Tools

Once configured, you can use these tools:

### Tool: `extract_text_from_file`

Extract complete text from a document file.

**Parameters:**
- `path` (string, required): Absolute or relative path to the document
- `max_pages` (int, optional): For PDFs, parse only the first N pages (default: 50, set to 0 to disable)
- `max_rows` (int, optional): For CSV/Excel, parse only N data rows (default: 500, set to 0 to disable)

**Returns:** Extracted text as string (automatically truncated at 100,000 characters by default)

**Supported formats:** `.pdf`, `.xlsx`, `.xlsm`, `.csv`, `.txt`, `.json`, `.md`, `.docx`

**Note:** For large files, use `extract_text_from_file_stream` instead to avoid memory issues.

**Default Limits:** To prevent AI context overflow, the tool applies sensible defaults:
- PDFs: First 50 pages
- Excel/CSV: First 500 rows
- All formats: 100,000 character output limit

### Tool: `extract_text_from_file_stream`

Stream text chunks from a document (memory-efficient for large files).

**Parameters:**
- `path` (string, required): Absolute or relative path to the document
- `max_pages` (int, optional): For PDFs, page cap (default: 50, set to 0 to disable)
- `max_rows` (int, optional): For CSV/Excel, row cap (default: 500, set to 0 to disable)
- `chunk_size` (int, optional): Characters per chunk (default: 4096, min: 512)

**Yields:** Text chunks as strings

**Supported formats:** All formats from `extract_text_from_file`

### Tool: `convert_to_markdown`

Convert various document formats to Markdown, extracting and saving images when applicable.

**⚠️ Important**: This tool converts the **ENTIRE document** and saves it to a file. It **ignores** the `DOC_READER_DEFAULT_MAX_ROWS`, `DOC_READER_DEFAULT_MAX_PAGES`, and `DOC_READER_MAX_OUTPUT_CHARS` environment variables. Only the preview returned to the AI is limited to protect context - the saved file contains the complete document.

**Parameters:**
- `path` (string, required): Absolute or relative path to the file to convert
- `output_dir` (string, optional): Directory where the markdown file and images will be saved. If not specified, saves in the same directory as the source file
- `output_filename` (string, optional): Name for the output markdown file (without extension). If not specified, uses the source filename with .md extension

**Returns:** Dictionary containing:
- `markdown_path`: Path to the saved markdown file (contains FULL content, not truncated)
- `images_dir`: Path to the directory containing extracted images (if any)
- `image_count`: Number of images extracted
- `markdown_preview`: First 500 characters preview (truncated for AI context protection)
- `file_size_chars`: Total character count of the saved markdown file
- `status`: "success" or error status
- `message`: Human-readable status message

**Supported formats:**
- PDF (`.pdf`) - with automatic image extraction and positioning at page locations
- Excel (`.xlsx`, `.xlsm`, `.xltx`, `.xltm`) - converted to markdown tables
- Word (`.docx`) - with image extraction
- CSV (`.csv`) - converted to markdown tables
- PowerPoint (`.pptx`) - text and images
- HTML (`.html`, `.htm`)
- Plain text (`.txt`, `.log`)
- Images (`.jpg`, `.jpeg`, `.png`) - with OCR if available

**Example Usage:**
```python
# Convert a Word document with images
result = convert_to_markdown(
    path="/path/to/document.docx",
    output_dir="/path/to/output"
)
# Creates: /path/to/output/document.md
#          /path/to/output/document_images/image_1.png
#          /path/to/output/document_images/image_2.png
```

**Important Notes:**
- **Full file is saved**: The complete markdown file is saved to disk without any truncation, regardless of size
- **Preview is truncated**: Only the preview returned to the AI is limited to 500 characters to protect context
- **Images**: Automatically extracted from supported formats and saved in a `{filename}_images/` subdirectory, with markdown using relative paths to reference them
- **PDF images**: Images are intelligently positioned throughout the markdown document at their corresponding page locations, making them viewable in preview

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

```
Convert the Word document ~/Documents/proposal.docx to Markdown and save it in ~/Documents/markdown/
```

```
Convert this Excel file to Markdown: ~/data/sales_report.xlsx
```

### Programmatic Usage:

```python
# Via MCP client - Extract text
result = await client.call_tool("extract_text_from_file", {
    "path": "/path/to/document.pdf",
    "max_pages": 5
})

# Streaming large files
async for chunk in client.stream_tool("extract_text_from_file_stream", {
    "path": "/path/to/large_file.csv",
    "chunk_size": 8192
}):
    print(chunk)

# Convert to Markdown
result = await client.call_tool("convert_to_markdown", {
    "path": "/path/to/document.docx",
    "output_dir": "/path/to/output",
    "output_filename": "converted_document"
})
print(f"Markdown saved to: {result['markdown_path']}")
print(f"Images extracted: {result['image_count']}")
```

## Configuration

### Environment Variables

Configure the server behavior using these environment variables:

- `DOC_READER_RATE_LIMIT_PER_MINUTE`: Maximum tool calls per minute (default: 60)
  - **Applies to**: All tools
  
- `DOC_READER_MAX_OUTPUT_CHARS`: Maximum output text size in characters (default: 100000)
  - **Applies to**: `extract_text_from_file` and `extract_text_from_file_stream` only
  - **Does NOT apply to**: `convert_to_markdown` (saves full file, only preview is limited)
  
- `DOC_READER_DEFAULT_MAX_ROWS`: Default maximum rows for spreadsheets/CSV (default: 500, set to 0 to disable)
  - **Applies to**: `extract_text_from_file` and `extract_text_from_file_stream` only
  - **Does NOT apply to**: `convert_to_markdown` (converts entire document)
  
- `DOC_READER_DEFAULT_MAX_PAGES`: Default maximum pages for PDFs (default: 50, set to 0 to disable)
  - **Applies to**: `extract_text_from_file` and `extract_text_from_file_stream` only
  - **Does NOT apply to**: `convert_to_markdown` (converts entire document)

**Example:**
```bash
export DOC_READER_RATE_LIMIT_PER_MINUTE=120
export DOC_READER_MAX_OUTPUT_CHARS=200000
export DOC_READER_DEFAULT_MAX_ROWS=1000
export DOC_READER_DEFAULT_MAX_PAGES=100
python -m server.main
```

**Why these limits?** 
Large documents can easily exceed AI model context windows (typically 200K-1M tokens). These defaults prevent context overflow while allowing flexibility for specific use cases. When limits are hit, the tool provides clear warnings with instructions on how to adjust them.

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
| PDF (text) | `pdfminer.six` | Included |
| PDF (images) | `pymupdf` | Included |
| Excel | `openpyxl` | Included |
| Word | `python-docx` | Included |
| CSV | `csv` (stdlib) | Built-in |
| TXT | File I/O (stdlib) | Built-in |
| JSON | `json` (stdlib) | Built-in |
| Markdown | File I/O (stdlib) | Built-in |
| **Conversion** | `markitdown` | Included |

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
- For PDF image extraction issues, ensure PyMuPDF is installed: `pip install pymupdf`

### Windows-specific issues

#### PowerShell execution policy error
If you see `cannot be loaded because running scripts is disabled`:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### Path length limitations (Windows)
Windows has a 260-character path limit by default. For long paths:
1. Enable long path support in Windows 10/11: [Microsoft Docs](https://learn.microsoft.com/en-us/windows/win32/fileio/maximum-file-path-limitation)
2. Or move the repository to a shorter path (e.g., `C:\mcp\document-reader`)

#### Python not found on Windows
- Ensure Python 3.10+ is installed and added to PATH
- Verify with: `python --version`
- If `python` doesn't work, try `py` or `python3`

#### Virtual environment activation issues on Windows
- Command Prompt: Use `.venv\Scripts\activate.bat`
- PowerShell: Use `.venv\Scripts\Activate.ps1`
- Git Bash: Use `source .venv/Scripts/activate`

### Docker-related issues

#### Docker not running
- Ensure Docker Desktop is installed and running
- On Windows, Docker Desktop requires WSL 2

#### Permission errors with Docker volumes
- On Windows, ensure the drive is shared in Docker Desktop settings
- Right-click Docker Desktop icon → Settings → Resources → File Sharing

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

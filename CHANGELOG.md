# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2025-10-17

### Added
- Initial release of document-reader-mcp
- Support for PDF file extraction using pdfminer.six
- Support for Excel files (.xlsx, .xlsm, .xltx, .xltm) using openpyxl
- Support for Word documents (.docx) using python-docx
- Support for CSV files with automatic encoding detection
- Support for plain text files (.txt, .log, .text)
- Support for JSON files with pretty-printing
- Support for Markdown files (.md, .markdown)
- Streaming API for memory-efficient processing of large files
- Rate limiting with configurable limits
- Smart encoding detection for text-based formats
- File size limit (100MB) for safety
- Comprehensive error handling and validation
- MCP tool implementations using FastMCP
- Docker support with Dockerfile and .dockerignore
- Documentation and usage examples
- GitHub issue templates and workflows
- **Markdown conversion tool**: New `convert_to_markdown` tool for converting documents to Markdown
  - Supports PDF, Excel, Word, CSV, PowerPoint, HTML, and image files
  - Automatic image extraction from PDFs and DOCX files
  - Images saved in `{filename}_images/` subdirectory with relative path references
  - Returns structured output with markdown path, image count, and preview
  - **Converts entire documents**: Ignores row/page/character limits (only preview is truncated)
- **Context overflow protection**: Automatic limits to prevent AI context exhaustion
  - Default 100,000 character output limit (configurable via `DOC_READER_MAX_OUTPUT_CHARS`)
  - Default 500 row limit for spreadsheets/CSV (configurable via `DOC_READER_DEFAULT_MAX_ROWS`)
  - Default 50 page limit for PDFs (configurable via `DOC_READER_DEFAULT_MAX_PAGES`)
  - **Applies only to extraction tools**, NOT to `convert_to_markdown` which saves full files
  - Clear warnings when limits are hit with instructions to adjust
- **markitdown library**: Integration with Microsoft's MarkItDown for document conversion
- **Cross-platform support**: Full Windows compatibility alongside macOS and Linux
- Windows setup scripts: `dev-setup.bat` for Command Prompt and `dev-setup.ps1` for PowerShell
- Comprehensive cross-platform documentation in `CROSS_PLATFORM.md`
- `.gitattributes` for consistent line endings across all platforms
- GitHub Actions CI/CD workflow testing on Windows, macOS, and Linux
- Platform-specific installation instructions in README and QUICK_START
- Windows-specific troubleshooting documentation
- Platform classifiers in setup.py for PyPI

### Changed
- **Extract tools now apply sensible defaults** to prevent context overflow
  - `max_pages` defaults to 50 for PDFs (previously unlimited)
  - `max_rows` defaults to 500 for spreadsheets/CSV (previously unlimited)
  - All text output truncated at 100,000 characters by default
- Tool documentation updated with default limit information
- README.md updated with Windows-specific configuration examples and new features
- QUICK_START.md updated with platform-specific setup instructions
- Documentation now includes Windows Command Prompt and PowerShell examples
- Enhanced error messages with actionable guidance

### Fixed
- **Large file context overflow**: Files like 3000+ row Excel sheets no longer consume entire AI context
- Streaming tools now respect character limits across all formats
- **Markdown conversion**: Full content is now saved to file (not truncated), only preview is limited for AI context protection

### Security
- Process-wide rate limiting to prevent abuse
- File size validation
- Path expansion with security considerations
- Safe error messages without exposing sensitive data
- Docker container runs as non-root user (UID 1000)
- Read-only volume mounts for document directories

### Technical Notes
- Zero code changes required in `server/main.py` - already cross-platform compatible
- All dependencies verified as cross-platform (pure Python)
- CI/CD tests on Python 3.10, 3.11, and 3.12 across all platforms
- Base64 image extraction from markdown data URIs for compatibility
- Smart truncation at line boundaries for cleaner output

[1.0.0]: https://github.com/ifmelate/document-reader-mcp/releases/tag/v1.0.0


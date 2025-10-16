# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **Cross-platform support**: Full Windows compatibility alongside macOS and Linux
- Windows setup scripts: `dev-setup.bat` for Command Prompt and `dev-setup.ps1` for PowerShell
- Comprehensive cross-platform documentation in `CROSS_PLATFORM.md`
- `.gitattributes` for consistent line endings across all platforms
- GitHub Actions CI/CD workflow testing on Windows, macOS, and Linux
- Platform-specific installation instructions in README and QUICK_START
- Windows-specific troubleshooting documentation
- Platform classifiers in setup.py for PyPI

### Changed
- README.md updated with Windows-specific configuration examples
- QUICK_START.md updated with platform-specific setup instructions
- Documentation now includes Windows Command Prompt and PowerShell examples

### Technical Notes
- Zero code changes required in `server/main.py` - already cross-platform compatible
- All dependencies verified as cross-platform (pure Python)
- CI/CD tests on Python 3.10, 3.11, and 3.12 across all platforms

## [1.0.0] - 2025-10-16

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
- Page limits for PDFs
- Row limits for CSV and Excel files
- Comprehensive error handling and validation
- MCP tool implementations using FastMCP
- Docker support with Dockerfile and .dockerignore
- Documentation and usage examples
- GitHub issue templates and workflows

### Security
- Process-wide rate limiting to prevent abuse
- File size validation
- Path expansion with security considerations
- Safe error messages without exposing sensitive data
- Docker container runs as non-root user (UID 1000)
- Read-only volume mounts for document directories

[1.0.0]: https://github.com/ifmelate/document-reader-mcp/releases/tag/v1.0.0


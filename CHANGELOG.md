# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
- Documentation and usage examples

### Security
- Process-wide rate limiting to prevent abuse
- File size validation
- Path expansion with security considerations
- Safe error messages without exposing sensitive data

[1.0.0]: https://github.com/ifmelate/document-reader-mcp/releases/tag/v1.0.0


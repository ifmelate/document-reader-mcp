# Security Policy

## Supported Versions

Currently supported versions with security updates:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Reporting a Vulnerability

We take the security of document-reader-mcp seriously. If you discover a security vulnerability, please follow these steps:

### 1. Do NOT Create a Public Issue

Security vulnerabilities should not be disclosed publicly until a fix is available.

### 2. Report Privately

Please report security vulnerabilities by:
- Opening a [GitHub Security Advisory](https://github.com/ifmelate/document-reader-mcp/security/advisories/new)
- Or emailing the maintainers directly (check GitHub profile for contact)

### 3. Include Details

In your report, please include:
- Description of the vulnerability
- Steps to reproduce the issue
- Potential impact
- Suggested fix (if you have one)
- Your contact information for follow-up

### 4. Response Timeline

We aim to:
- Acknowledge receipt within 48 hours
- Provide an initial assessment within 7 days
- Release a fix within 30 days for critical issues

### 5. Coordinated Disclosure

We request that you:
- Give us reasonable time to address the issue
- Do not publicly disclose the vulnerability until we release a fix
- Do not exploit the vulnerability maliciously

## Security Considerations

### File System Access

⚠️ **Important**: This MCP server reads files from the local filesystem. Be aware:

- **Do NOT expose to untrusted networks**: This server is designed for local use only
- **Trusted environments only**: Use only with trusted MCP clients (e.g., Cursor IDE, Claude Desktop)
- **No authentication**: There is no built-in authentication mechanism
- **Rate limiting**: Rate limits are per-process, not per-user
- **Path validation**: File paths are validated but expanded with `os.path.expanduser()`

### File Size Limits

- Maximum file size: **100 MB** (enforced to prevent resource exhaustion)
- This limit cannot be bypassed without code modification

### Rate Limiting

- Default: 60 requests per minute per process
- Configurable via `DOC_READER_RATE_LIMIT_PER_MINUTE` environment variable
- Not suitable for multi-user or high-security environments

### Dependencies

We use well-established libraries:
- `fastmcp` for MCP protocol implementation
- `pdfminer.six` for PDF processing
- `openpyxl` for Excel files
- `python-docx` for Word documents

All dependencies are specified with minimum versions in `requirements.txt`.

### Best Practices

When deploying this server:

1. **Isolation**: Run in an isolated environment (container, VM, or sandboxed process)
2. **Least Privilege**: Run with minimal file system permissions
3. **Network Isolation**: Do not expose stdio interface to network sockets
4. **Input Validation**: The server validates file paths and sizes, but be aware of the files it can access
5. **Monitoring**: Monitor rate limiting and resource usage
6. **Updates**: Keep dependencies updated to receive security patches

## Known Limitations

- No user authentication or authorization
- Rate limiting is process-wide, not per-user
- File access is limited only by OS permissions of the running process
- No sandboxing of document parsers (relies on underlying libraries)

## Updates

Security updates will be announced via:
- GitHub Security Advisories
- Release notes in CHANGELOG.md
- GitHub Releases page

## Questions?

For non-security-related questions about this policy, please open a regular GitHub issue.


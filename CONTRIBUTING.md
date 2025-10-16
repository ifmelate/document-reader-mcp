# Contributing to document-reader-mcp

Thank you for considering contributing to document-reader-mcp! This guide will help you get started.

## Development Setup

### 1. Fork and Clone

```bash
git clone https://github.com/ifmelate/document-reader-mcp.git
cd document-reader-mcp
```

### 2. Create Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Test the Server

```bash
python -m server.main
```

The server should start and be ready to accept MCP requests over stdio.

## Code Style

This project follows these conventions:

- **Python**: PEP 8 with 4-space indentation
- **EditorConfig**: Respect `.editorconfig` settings
- **Commit Messages**: Use [Conventional Commits](https://www.conventionalcommits.org/)
  - `feat:` for new features
  - `fix:` for bug fixes
  - `docs:` for documentation updates
  - `refactor:` for code refactoring
  - `test:` for test additions/changes
  - `chore:` for maintenance tasks

## Adding Support for a New File Format

To add a new document format:

1. **Create an extraction function** in `server/main.py`:
   ```python
   def _extract_text_from_<format>(path: str, **kwargs) -> str:
       """Extract text from <format> file."""
       # Implementation here
       pass
   ```

2. **Add format routing** in `extract_text_from_file()`:
   ```python
   elif ext_lower == ".<format>":
       text = _extract_text_from_<format>(expanded_path)
   ```

3. **Add streaming support** in `extract_text_from_file_stream()`:
   ```python
   elif ext_lower == ".<format>":
       # Stream implementation here
       pass
   ```

4. **Update documentation**:
   - Add format to README.md supported formats table
   - Update docstrings in tool functions
   - Add any new dependencies to `requirements.txt`

5. **Test thoroughly**:
   - Test with various sample files
   - Test edge cases (empty files, large files, malformed files)
   - Verify rate limiting works correctly

## Pull Request Process

1. **Create a feature branch** from `main`:
   ```bash
   git checkout -b feat/add-xyz-support
   ```

2. **Make your changes** following the code style guidelines

3. **Test your changes** thoroughly:
   - Test basic functionality
   - Test error handling
   - Test with edge cases

4. **Commit with conventional commit messages**:
   ```bash
   git commit -m "feat: add support for XYZ file format"
   ```

5. **Push and create a pull request**:
   ```bash
   git push origin feat/add-xyz-support
   ```

6. **Describe your changes** in the PR:
   - What problem does it solve?
   - How did you test it?
   - Any breaking changes?
   - Screenshots/examples if applicable

## Code Review

All submissions require review. We'll review:

- Code quality and maintainability
- Test coverage
- Documentation updates
- Security considerations
- Performance implications

## Security

If you discover a security vulnerability:

1. **Do NOT open a public issue**
2. Email details to the maintainers privately
3. Wait for confirmation before disclosing

## Questions?

- Open an issue for bugs or feature requests
- Start a discussion for general questions
- Check existing issues before creating new ones

## License

By contributing, you agree that your contributions will be licensed under the MIT License.


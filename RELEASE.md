# Release Guide

This guide describes how to create a new release of document-reader-mcp.

## Pre-release Checklist

### 1. Version Update
- [ ] Update version in `server/__version__.py`
- [ ] Update version in `setup.py`
- [ ] Update version in `README.md` (bottom section)
- [ ] Add entry to `CHANGELOG.md` with release date

### 2. Documentation Review
- [ ] Ensure README.md is up to date
- [ ] Verify all examples work
- [ ] Check that installation instructions are accurate
- [ ] Review CONTRIBUTING.md for accuracy

### 3. Code Quality
- [ ] Run syntax checks: `python -m py_compile server/*.py`
- [ ] Test server imports: `python -c "from server.main import server"`
- [ ] Verify all dependencies in `requirements.txt` are necessary
- [ ] Check for security vulnerabilities in dependencies

### 4. Testing
- [ ] Test with sample PDF files
- [ ] Test with Excel files
- [ ] Test with CSV files
- [ ] Test with Word documents
- [ ] Test with text, JSON, and Markdown files
- [ ] Test rate limiting functionality
- [ ] Test streaming for large files
- [ ] Test error handling (invalid files, missing files, etc.)
- [ ] Test in Cursor or Claude Desktop

## Release Process

### 1. Prepare the Release

```bash
# Ensure you're on main branch
git checkout main
git pull origin main

# Verify clean working directory
git status
```

### 2. Update Version Files

Edit the following files with the new version number:
- `server/__version__.py`
- `setup.py`
- `README.md`

Update `CHANGELOG.md` with:
- Release date
- Summary of changes
- Links to issues/PRs

### 3. Commit Version Changes

```bash
git add server/__version__.py setup.py README.md CHANGELOG.md
git commit -m "chore: bump version to X.Y.Z"
git push origin main
```

### 4. Create Git Tag

```bash
# Create annotated tag
git tag -a vX.Y.Z -m "Release version X.Y.Z"

# Push tag to GitHub
git push origin vX.Y.Z
```

### 5. Create GitHub Release

1. Go to https://github.com/ifmelate/document-reader-mcp/releases/new
2. Select the tag you just created (vX.Y.Z)
3. Set release title: "v X.Y.Z"
4. Copy relevant section from CHANGELOG.md to release notes
5. Attach any additional assets if needed
6. Click "Publish release"

### 6. Verify Release

- [ ] GitHub release is published
- [ ] Tag is visible in repository
- [ ] Installation via pip works: `pip install git+https://github.com/ifmelate/document-reader-mcp.git@vX.Y.Z`
- [ ] Documentation links work correctly

## Post-release

### 1. Announce
- Consider posting in relevant communities (if applicable)
- Update any external documentation or listings

### 2. Monitor
- Watch for issues on GitHub
- Monitor installation feedback
- Check for dependency updates

## Hotfix Process

For critical bugs requiring immediate release:

1. Create hotfix branch from main:
   ```bash
   git checkout -b hotfix/vX.Y.Z+1
   ```

2. Fix the issue and test thoroughly

3. Update version (increment patch number)

4. Follow normal release process

## Version Numbering

We follow [Semantic Versioning](https://semver.org/):

- **MAJOR** (X.0.0): Breaking changes
- **MINOR** (x.Y.0): New features, backwards compatible
- **PATCH** (x.y.Z): Bug fixes, backwards compatible

## Support Policy

- Latest stable version receives all updates
- Previous minor version may receive critical security patches
- Older versions are not actively supported

## Questions?

Open an issue on GitHub for release-related questions.


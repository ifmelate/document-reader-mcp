# GitHub Release Steps

This document provides step-by-step instructions to release document-reader-mcp on GitHub.

## Prerequisites

✅ All release-ready checks have passed  
✅ Repository is clean (no uncommitted changes)  
✅ All tests pass locally  
✅ Documentation is up to date  

## Steps to Release on GitHub

### 1. Initialize Git Repository (if not done)

```bash
cd /Users/work/document-reader-mcp
git init
git add .
git commit -m "chore: initial commit - v1.0.0"
```

### 2. Create GitHub Repository

1. Go to https://github.com/new
2. Set repository name: `document-reader-mcp`
3. Set description: "Universal MCP server for extracting text from various document formats"
4. Choose: **Public** (or Private if you prefer)
5. **Do NOT** initialize with README, .gitignore, or license (we already have these)
6. Click "Create repository"

### 3. Connect Local Repository to GitHub

```bash
# Add GitHub as remote
git remote add origin https://github.com/ifmelate/document-reader-mcp.git

# Verify remote
git remote -v

# Push to GitHub
git branch -M main
git push -u origin main
```

### 4. Configure Repository Settings

Go to your repository settings on GitHub:

#### General Settings
- ✓ Description: "Universal MCP server for extracting text from various document formats"
- ✓ Website: (optional)
- ✓ Topics: `mcp`, `document-reader`, `pdf`, `excel`, `csv`, `python`, `mcp-server`

#### Features
- ✓ Enable Issues
- ✓ Enable Discussions (recommended)
- ✓ Enable Wiki (optional)

#### Security
- Go to Settings → Security → Code security and analysis
- ✓ Enable Dependabot alerts
- ✓ Enable Dependabot security updates

### 5. Create First Release

#### Option A: Via GitHub Web Interface

1. Go to https://github.com/ifmelate/document-reader-mcp/releases/new
2. Click "Choose a tag" and type: `v1.0.0`
3. Click "Create new tag: v1.0.0 on publish"
4. Set Release title: `v1.0.0`
5. Copy this release description:

```markdown
# Initial Release 🎉

First stable release of document-reader-mcp - a universal MCP server for extracting text from various document formats.

## Features

✅ **Multiple format support**: PDF, Excel, CSV, TXT, JSON, Markdown, DOCX  
✅ **Streaming API**: Memory-efficient processing of large files  
✅ **Smart encoding detection**: Handles UTF-8, Latin-1, CP1252, ISO-8859-1  
✅ **Rate limiting**: Configurable process-wide rate limiting  
✅ **Modular design**: Easy to extend with new formats  

## Supported Formats

- PDF (`.pdf`)
- Excel (`.xlsx`, `.xlsm`, `.xltx`, `.xltm`)
- Word (`.docx`)
- CSV (`.csv`)
- Plain Text (`.txt`, `.log`, `.text`)
- JSON (`.json`)
- Markdown (`.md`, `.markdown`)

## Installation

```bash
git clone https://github.com/ifmelate/document-reader-mcp.git
cd document-reader-mcp
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Quick Start

See [QUICK_START.md](QUICK_START.md) for detailed setup instructions.

## Documentation

- [README.md](README.md) - Full documentation
- [CONTRIBUTING.md](CONTRIBUTING.md) - Contribution guidelines
- [SECURITY.md](SECURITY.md) - Security policy

## What's Changed

See [CHANGELOG.md](CHANGELOG.md) for full details.
```

6. Click "Publish release"

#### Option B: Via Command Line

```bash
# Create and push tag
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0

# Then create release via GitHub web interface as described above
```

### 6. Verify Release

After publishing, verify:

- [ ] Release appears on https://github.com/ifmelate/document-reader-mcp/releases
- [ ] Tag `v1.0.0` is visible
- [ ] Repository shows current version
- [ ] README displays correctly on GitHub
- [ ] Installation works: `pip install git+https://github.com/ifmelate/document-reader-mcp.git`

### 7. Update Repository Metadata

Add these topics to your repository (Settings → General → Topics):
- `mcp`
- `mcp-server`
- `document-reader`
- `pdf-extraction`
- `excel-parser`
- `csv-parser`
- `python`
- `fastmcp`

### 8. Create Initial GitHub Discussions (Optional)

Navigate to Discussions tab and create categories:
- 📢 Announcements
- 💡 Ideas
- 🙏 Q&A
- 🗣️ General

Post welcome message in Announcements.

### 9. Set Up GitHub Pages (Optional)

If you want to host documentation:

1. Go to Settings → Pages
2. Source: Deploy from branch `main`
3. Folder: `/` (root)
4. Save

## Post-Release Tasks

### Announce the Release

Consider announcing in:
- [ ] GitHub Discussions
- [ ] Social media (if applicable)
- [ ] Relevant communities or forums
- [ ] MCP community channels

### Monitor

- [ ] Watch for new issues
- [ ] Respond to installation questions
- [ ] Monitor GitHub Actions (if any fail)
- [ ] Check Dependabot alerts

### Optional: Create Release Notes Template

For future releases, create `.github/RELEASE_TEMPLATE.md`:

```markdown
## What's Changed

### Added
- 

### Fixed
- 

### Changed
- 

### Security
- 

**Full Changelog**: https://github.com/ifmelate/document-reader-mcp/compare/vX.Y.Z...vX.Y.Z+1
```

## Future Releases

For subsequent releases, follow the process in [RELEASE.md](RELEASE.md).

## Troubleshooting

### "remote: Permission denied"
- Verify your GitHub authentication (SSH key or personal access token)
- Check you have write access to the repository

### "failed to push some refs"
- Pull latest changes first: `git pull origin main --rebase`
- Then push: `git push origin main`

### Tag Already Exists
- Delete local tag: `git tag -d v1.0.0`
- Delete remote tag: `git push origin --delete v1.0.0`
- Create new tag

## Questions?

Open an issue at https://github.com/ifmelate/document-reader-mcp/issues


#!/bin/bash
# Development setup script for document-reader-mcp

set -e

echo "=== document-reader-mcp Development Setup ==="
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
else
    echo "Virtual environment already exists"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Verify installation
echo ""
echo "Verifying installation..."
python -c "from server.main import server; from server.__version__ import __version__; print(f'✓ Server v{__version__} imported successfully')"

echo ""
echo "=== Setup Complete ==="
echo ""
echo "To activate the environment, run:"
echo "  source .venv/bin/activate"
echo ""
echo "To start the server, run:"
echo "  python -m server.main"
echo ""


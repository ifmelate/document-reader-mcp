#!/bin/bash
# Check if the repository is ready for GitHub release

set -e

echo "=== Checking if repository is ready for GitHub release ==="
echo ""

ERRORS=0
WARNINGS=0

# Function to check file exists
check_file() {
    if [ -f "$1" ]; then
        echo "✓ $1"
    else
        echo "✗ MISSING: $1"
        ((ERRORS++))
    fi
}

# Function to check directory exists
check_dir() {
    if [ -d "$1" ]; then
        echo "✓ $1/"
    else
        echo "✗ MISSING: $1/"
        ((ERRORS++))
    fi
}

# Check essential files
echo "Checking essential files..."
check_file "README.md"
check_file "LICENSE"
check_file "requirements.txt"
check_file "setup.py"
check_file ".gitignore"
check_file ".editorconfig"
echo ""

# Check documentation files
echo "Checking documentation..."
check_file "CONTRIBUTING.md"
check_file "CHANGELOG.md"
check_file "SECURITY.md"
check_file "CODE_OF_CONDUCT.md"
check_file "RELEASE.md"
echo ""

# Check server files
echo "Checking server files..."
check_dir "server"
check_file "server/__init__.py"
check_file "server/main.py"
check_file "server/__version__.py"
echo ""

# Check GitHub templates
echo "Checking GitHub templates..."
check_dir ".github"
check_dir ".github/ISSUE_TEMPLATE"
check_file ".github/ISSUE_TEMPLATE/bug_report.md"
check_file ".github/ISSUE_TEMPLATE/feature_request.md"
check_file ".github/pull_request_template.md"
check_dir ".github/workflows"
check_file ".github/workflows/validate.yml"
echo ""

# Check version consistency
echo "Checking version consistency..."
if [ -f "server/__version__.py" ]; then
    VERSION=$(grep "__version__" server/__version__.py | cut -d'"' -f2)
    echo "Version in __version__.py: $VERSION"
    
    if grep -q "version=\"$VERSION\"" setup.py; then
        echo "✓ Version matches in setup.py"
    else
        echo "⚠ WARNING: Version mismatch in setup.py"
        ((WARNINGS++))
    fi
    
    if grep -q "version-$VERSION" README.md; then
        echo "✓ Version mentioned in README.md"
    else
        echo "⚠ WARNING: Version not found in README.md"
        ((WARNINGS++))
    fi
else
    echo "✗ Cannot check version"
    ((ERRORS++))
fi
echo ""

# Check for sensitive data
echo "Checking for sensitive data..."
if grep -r "password\|secret\|api_key\|token" --exclude-dir=.git --exclude-dir=.venv --exclude="*.sh" . | grep -v "SECURITY.md\|README.md\|CONTRIBUTING.md" > /dev/null; then
    echo "⚠ WARNING: Found potential sensitive keywords (please verify manually)"
    ((WARNINGS++))
else
    echo "✓ No obvious sensitive data patterns found"
fi
echo ""

# Check Python syntax if Python is available
echo "Checking Python syntax..."
if command -v python3 &> /dev/null; then
    if python3 -m py_compile server/__init__.py server/main.py server/__version__.py 2>/dev/null; then
        echo "✓ All Python files compile successfully"
    else
        echo "✗ Python syntax errors found"
        ((ERRORS++))
    fi
else
    echo "⚠ Python3 not found, skipping syntax check"
    ((WARNINGS++))
fi
echo ""

# Summary
echo "=== Summary ==="
echo "Errors: $ERRORS"
echo "Warnings: $WARNINGS"
echo ""

if [ $ERRORS -eq 0 ]; then
    if [ $WARNINGS -eq 0 ]; then
        echo "✓ Repository is ready for GitHub release!"
        exit 0
    else
        echo "⚠ Repository is mostly ready, but please review warnings"
        exit 0
    fi
else
    echo "✗ Repository is NOT ready for release. Please fix errors."
    exit 1
fi


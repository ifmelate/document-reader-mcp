"""Setup configuration for document-reader-mcp."""
from pathlib import Path
from setuptools import setup, find_packages

# Read the README for the long description
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="document-reader-mcp",
    version="1.0.0",
    description="Universal MCP server for extracting text from various document formats",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="ifmelate",
    url="https://github.com/ifmelate/document-reader-mcp",
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[
        "mcp>=1.1.0",
        "fastmcp>=2.0.0",
        "pdfminer.six>=20221105",
        "openpyxl>=3.1.0",
        "python-docx>=1.0.0",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries",
        "Topic :: Text Processing",
    ],
    keywords="mcp document reader pdf excel csv docx",
    project_urls={
        "Source": "https://github.com/ifmelate/document-reader-mcp",
        "Bug Reports": "https://github.com/ifmelate/document-reader-mcp/issues",
    },
)


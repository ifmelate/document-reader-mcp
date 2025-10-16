import os
import time
import asyncio
import csv
import json
from collections import deque
from typing import Optional, AsyncGenerator, Deque
from pathlib import Path

from fastmcp import FastMCP

from server.__version__ import __version__

try:
    from pdfminer.high_level import extract_text as pdf_extract_text
except Exception:  # pragma: no cover
    pdf_extract_text = None

try:
    from openpyxl import load_workbook
except Exception:  # pragma: no cover
    load_workbook = None

try:
    import docx
except Exception:  # pragma: no cover
    docx = None

try:
    import markdown
except Exception:  # pragma: no cover
    markdown = None


server = FastMCP("document-reader-mcp")


class SimpleRateLimiter:
    """In-memory sliding-window rate limiter (process-wide).

    Not suitable for multi-process or distributed deployments.
    """

    def __init__(self, max_calls: int, window_seconds: int = 60) -> None:
        self.max_calls = max_calls
        self.window_seconds = window_seconds
        self._timestamps: Deque[float] = deque()

    def allow(self) -> bool:
        now = time.time()
        window_start = now - self.window_seconds
        while self._timestamps and self._timestamps[0] < window_start:
            self._timestamps.popleft()
        if len(self._timestamps) >= self.max_calls:
            return False
        self._timestamps.append(now)
        return True


_rate_limit_per_minute_env = os.getenv("DOC_READER_RATE_LIMIT_PER_MINUTE", "60")
try:
    _rate_limit_per_minute = max(1, int(_rate_limit_per_minute_env))
except ValueError:
    _rate_limit_per_minute = 60

_rate_limiter = SimpleRateLimiter(max_calls=_rate_limit_per_minute, window_seconds=60)


def _enforce_rate_limit() -> None:
    if not _rate_limiter.allow():
        raise RuntimeError("Rate limit exceeded. Try again later or increase limits in configuration.")


def _extract_text_from_pdf(path: str, max_pages: Optional[int] = None) -> str:
    if pdf_extract_text is None:
        raise RuntimeError(
            "pdfminer.six is not installed. To process PDF files, install it with: "
            "pip install pdfminer.six"
        )
    # Use pdfminer's maxpages to avoid parsing the whole file when limited
    maxpages_arg = 0 if not max_pages or max_pages <= 0 else int(max_pages)
    return pdf_extract_text(path, maxpages=maxpages_arg)


def _extract_text_from_xlsx(path: str, max_rows: Optional[int] = None) -> str:
    if load_workbook is None:
        raise RuntimeError(
            "openpyxl is not installed. To process Excel files, install it with: "
            "pip install openpyxl"
        )
    workbook = load_workbook(filename=path, data_only=True, read_only=True)
    try:
        lines: list[str] = []
        rows_emitted = 0
        for sheet in workbook.worksheets:
            lines.append(f"# Sheet: {sheet.title}")
            for row in sheet.iter_rows(values_only=True):
                values = ["" if cell is None else str(cell) for cell in row]
                line = "\t".join(values).rstrip()
                if line:
                    lines.append(line)
                    rows_emitted += 1
                    if max_rows is not None and max_rows > 0 and rows_emitted >= max_rows:
                        return "\n".join(lines).strip()
            lines.append("")
        return "\n".join(lines).strip()
    finally:
        workbook.close()


def _extract_text_from_csv(path: str, max_rows: Optional[int] = None) -> str:
    """Extract text from CSV file using Python's built-in csv module."""
    lines: list[str] = []
    rows_read = 0
    
    # Try different encodings to handle various CSV files
    encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
    
    for encoding in encodings:
        try:
            with open(path, 'r', encoding=encoding, newline='') as f:
                reader = csv.reader(f)
                for row in reader:
                    line = "\t".join(str(cell) for cell in row).rstrip()
                    if line:
                        lines.append(line)
                        rows_read += 1
                        if max_rows is not None and max_rows > 0 and rows_read >= max_rows:
                            break
            return "\n".join(lines).strip()
        except (UnicodeDecodeError, UnicodeError):
            continue
        except Exception as e:
            if encoding == encodings[-1]:  # Last encoding attempt
                raise RuntimeError(f"Failed to read CSV file: {e}") from e
    
    if not lines:
        raise RuntimeError("Failed to decode CSV file with any supported encoding")
    
    return "\n".join(lines).strip()


def _extract_text_from_txt(path: str) -> str:
    """Extract text from plain text file."""
    encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
    
    for encoding in encodings:
        try:
            with open(path, 'r', encoding=encoding) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
        except Exception as e:
            if encoding == encodings[-1]:
                raise RuntimeError(f"Failed to read text file: {e}") from e
    
    raise RuntimeError("Failed to decode text file with any supported encoding")


def _extract_text_from_json(path: str) -> str:
    """Extract text from JSON file (pretty-printed)."""
    encodings = ['utf-8', 'latin-1', 'cp1252']
    
    for encoding in encodings:
        try:
            with open(path, 'r', encoding=encoding) as f:
                data = json.load(f)
                return json.dumps(data, indent=2, ensure_ascii=False)
        except (UnicodeDecodeError, UnicodeError):
            continue
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON file: {e}") from e
        except Exception as e:
            if encoding == encodings[-1]:
                raise RuntimeError(f"Failed to read JSON file: {e}") from e
    
    raise RuntimeError("Failed to decode JSON file with any supported encoding")


def _extract_text_from_markdown(path: str) -> str:
    """Extract text from Markdown file (as plain text or HTML)."""
    encodings = ['utf-8', 'latin-1', 'cp1252']
    
    for encoding in encodings:
        try:
            with open(path, 'r', encoding=encoding) as f:
                md_content = f.read()
                
            # If markdown library is available, optionally convert to HTML
            # For simplicity, return plain markdown text
            return md_content
        except (UnicodeDecodeError, UnicodeError):
            continue
        except Exception as e:
            if encoding == encodings[-1]:
                raise RuntimeError(f"Failed to read Markdown file: {e}") from e
    
    raise RuntimeError("Failed to decode Markdown file with any supported encoding")


def _extract_text_from_docx(path: str) -> str:
    """Extract text from DOCX file."""
    if docx is None:
        raise RuntimeError(
            "python-docx is not installed. To process .docx files, install it with: "
            "pip install python-docx"
        )
    
    try:
        doc = docx.Document(path)
        paragraphs = [para.text for para in doc.paragraphs if para.text.strip()]
        return "\n".join(paragraphs)
    except Exception as e:
        raise RuntimeError(f"Failed to extract text from DOCX: {e}") from e


@server.tool
def extract_text_from_file(
    path: str,
    max_pages: Optional[int] = None,
    max_rows: Optional[int] = None,
) -> str:
    """
    Extract plain text from local document files.

    Supported formats:
    - PDF (.pdf)
    - Excel (.xlsx, .xlsm, .xltx, .xltm)
    - Word (.docx)
    - CSV (.csv)
    - Plain text (.txt, .log, .text)
    - JSON (.json)
    - Markdown (.md, .markdown)

    Args:
        path: Absolute or relative file path on the local machine.
        max_pages: For PDFs, parse only the first N pages (0 or None means no explicit
            page cap).
        max_rows: For spreadsheets and CSV, parse only N data rows across all sheets (0 or
            None means no explicit row cap).

    Returns:
        Extracted plain text as a string.
    """
    _enforce_rate_limit()
    if not path or not isinstance(path, str):
        raise ValueError("path must be a non-empty string")

    expanded_path = os.path.expanduser(path)
    if not os.path.isfile(expanded_path):
        raise FileNotFoundError(f"File not found: {expanded_path}")

    file_size = os.path.getsize(expanded_path)
    if file_size > 100 * 1024 * 1024:
        raise ValueError("File too large; limit is 100MB")

    _, ext = os.path.splitext(expanded_path)
    ext_lower = ext.lower()

    # Route to appropriate extractor based on file extension
    if ext_lower == ".pdf":
        text = _extract_text_from_pdf(expanded_path, max_pages=max_pages)
    elif ext_lower in (".xlsx", ".xlsm", ".xltx", ".xltm"):
        text = _extract_text_from_xlsx(expanded_path, max_rows=max_rows)
    elif ext_lower == ".csv":
        text = _extract_text_from_csv(expanded_path, max_rows=max_rows)
    elif ext_lower in (".txt", ".log", ".text"):
        text = _extract_text_from_txt(expanded_path)
    elif ext_lower == ".json":
        text = _extract_text_from_json(expanded_path)
    elif ext_lower in (".md", ".markdown"):
        text = _extract_text_from_markdown(expanded_path)
    elif ext_lower == ".docx":
        text = _extract_text_from_docx(expanded_path)
    else:
        raise ValueError(
            f"Unsupported file type: {ext_lower}. "
            f"Supported: .pdf, .xlsx, .csv, .txt, .json, .md, .docx"
        )

    return text


@server.tool
async def extract_text_from_file_stream(
    path: str,
    max_pages: Optional[int] = None,
    max_rows: Optional[int] = None,
    chunk_size: int = 4096,
) -> AsyncGenerator[str, None]:
    """
    Stream plain text chunks from local document files.

    Supported formats: PDF, Excel, CSV, TXT, JSON, Markdown, DOCX

    Args:
        path: Absolute or relative file path on the local machine.
        max_pages: For PDFs, page cap for parsing (0 or None means no explicit cap).
        max_rows: For spreadsheets and CSV, row cap across all sheets (0 or None means no explicit cap).
        chunk_size: Approximate maximum characters per streamed chunk. Actual chunk sizes may
            vary slightly.

    Yields:
        Text chunks as strings until the entire document (or capped portion) has been sent.
    """
    _enforce_rate_limit()
    if not path or not isinstance(path, str):
        raise ValueError("path must be a non-empty string")

    expanded_path = os.path.expanduser(path)
    if not os.path.isfile(expanded_path):
        raise FileNotFoundError(f"File not found: {expanded_path}")

    file_size = os.path.getsize(expanded_path)
    if file_size > 100 * 1024 * 1024:
        raise ValueError("File too large; limit is 100MB")

    _, ext = os.path.splitext(expanded_path)
    ext_lower = ext.lower()
    chunk_size = max(512, int(chunk_size))

    if ext_lower == ".pdf":
        # Extract text upfront with page cap, then stream in fixed-size chunks
        text = _extract_text_from_pdf(expanded_path, max_pages=max_pages)
        for i in range(0, len(text), chunk_size):
            yield text[i : i + chunk_size]
            await asyncio.sleep(0)
            
    elif ext_lower in (".xlsx", ".xlsm", ".xltx", ".xltm"):
        # Stream rows as they are read, accumulating into approx chunk_size blocks
        if load_workbook is None:
            raise RuntimeError(
                "openpyxl is not installed. To process Excel files, install it with: "
                "pip install openpyxl"
            )
        workbook = load_workbook(filename=expanded_path, data_only=True, read_only=True)
        try:
            buffer_lines: list[str] = []
            buffer_len = 0
            rows_emitted = 0
            for sheet in workbook.worksheets:
                header = f"# Sheet: {sheet.title}"
                if buffer_len + len(header) + 1 > chunk_size and buffer_lines:
                    yield "\n".join(buffer_lines)
                    buffer_lines = []
                    buffer_len = 0
                    await asyncio.sleep(0)
                buffer_lines.append(header)
                buffer_len += len(header) + 1

                for row in sheet.iter_rows(values_only=True):
                    values = ["" if cell is None else str(cell) for cell in row]
                    line = "\t".join(values).rstrip()
                    if not line:
                        continue
                    if buffer_len + len(line) + 1 > chunk_size and buffer_lines:
                        yield "\n".join(buffer_lines)
                        buffer_lines = []
                        buffer_len = 0
                        await asyncio.sleep(0)
                    buffer_lines.append(line)
                    buffer_len += len(line) + 1
                    rows_emitted += 1
                    if max_rows is not None and max_rows > 0 and rows_emitted >= max_rows:
                        break
                if max_rows is not None and max_rows > 0 and rows_emitted >= max_rows:
                    break
            if buffer_lines:
                yield "\n".join(buffer_lines)
        finally:
            workbook.close()
            
    elif ext_lower == ".csv":
        # Stream CSV rows with buffering
        encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
        success = False
        
        for encoding in encodings:
            try:
                buffer_lines: list[str] = []
                buffer_len = 0
                rows_emitted = 0
                
                with open(expanded_path, 'r', encoding=encoding, newline='') as f:
                    reader = csv.reader(f)
                    for row in reader:
                        line = "\t".join(str(cell) for cell in row).rstrip()
                        if not line:
                            continue
                        if buffer_len + len(line) + 1 > chunk_size and buffer_lines:
                            yield "\n".join(buffer_lines)
                            buffer_lines = []
                            buffer_len = 0
                            await asyncio.sleep(0)
                        buffer_lines.append(line)
                        buffer_len += len(line) + 1
                        rows_emitted += 1
                        if max_rows is not None and max_rows > 0 and rows_emitted >= max_rows:
                            break
                    
                    if buffer_lines:
                        yield "\n".join(buffer_lines)
                success = True
                break
            except (UnicodeDecodeError, UnicodeError):
                continue
                
        if not success:
            raise RuntimeError("Failed to decode CSV file with any supported encoding")
            
    elif ext_lower in (".txt", ".log", ".text", ".md", ".markdown"):
        # Stream text files in chunks
        encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
        success = False
        
        for encoding in encodings:
            try:
                with open(expanded_path, 'r', encoding=encoding) as f:
                    while True:
                        chunk = f.read(chunk_size)
                        if not chunk:
                            break
                        yield chunk
                        await asyncio.sleep(0)
                success = True
                break
            except (UnicodeDecodeError, UnicodeError):
                continue
                
        if not success:
            raise RuntimeError("Failed to decode text file with any supported encoding")
            
    elif ext_lower == ".json":
        # For JSON, extract all then stream in chunks (can't partially parse JSON)
        text = _extract_text_from_json(expanded_path)
        for i in range(0, len(text), chunk_size):
            yield text[i : i + chunk_size]
            await asyncio.sleep(0)
            
    elif ext_lower == ".docx":
        # For DOCX, extract all then stream in chunks
        text = _extract_text_from_docx(expanded_path)
        for i in range(0, len(text), chunk_size):
            yield text[i : i + chunk_size]
            await asyncio.sleep(0)
            
    else:
        raise ValueError(
            f"Unsupported file type: {ext_lower}. "
            f"Supported: .pdf, .xlsx, .csv, .txt, .json, .md, .docx"
        )




if __name__ == "__main__":
    server.run()

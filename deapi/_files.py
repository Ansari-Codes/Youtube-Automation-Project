from __future__ import annotations

import mimetypes
from pathlib import Path
from typing import BinaryIO, Union

# Types accepted for file parameters
FileInput = Union[str, Path, bytes, BinaryIO]


def normalize_file(file: FileInput, param_name: str = "file") -> tuple[str, bytes, str]:
    """Convert various file input types to httpx's expected tuple format.

    Returns:
        (filename, file_bytes, content_type)
    """
    if isinstance(file, (str, Path)):
        path = Path(file)
        content_type = mimetypes.guess_type(str(path))[0] or "application/octet-stream"
        return (path.name, path.read_bytes(), content_type)

    if isinstance(file, bytes):
        return (f"{param_name}.bin", file, "application/octet-stream")

    # BinaryIO / file-like object
    name = getattr(file, "name", None)
    if isinstance(name, str):
        filename = Path(name).name
        content_type = mimetypes.guess_type(filename)[0] or "application/octet-stream"
    else:
        filename = f"{param_name}.bin"
        content_type = "application/octet-stream"

    data = file.read()
    return (filename, data, content_type)


def normalize_files(
    files: list[FileInput] | FileInput,
    param_name: str = "file",
) -> list[tuple[str, bytes, str]]:
    """Normalize a single file or list of files."""
    if not isinstance(files, list):
        return [normalize_file(files, param_name)]
    return [normalize_file(f, param_name) for f in files]

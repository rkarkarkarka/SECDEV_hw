from __future__ import annotations

import uuid
from pathlib import Path

from src.shared import errors

MAX_BYTES = 5_000_000  # 5 MB
ALLOWED_TYPES = {"image/png", "image/jpeg"}

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
JPEG_SOI = b"\xff\xd8"
JPEG_EOI = b"\xff\xd9"


def sniff_image_type(data: bytes) -> str | None:
    if data.startswith(PNG_MAGIC):
        return "image/png"
    if data.startswith(JPEG_SOI) and data.endswith(JPEG_EOI):
        return "image/jpeg"
    return None


def secure_save(base_dir: str, data: bytes) -> str:
    if len(data) > MAX_BYTES:
        raise errors.ValidationError(detail="attachment too large")
    media_type = sniff_image_type(data)
    if media_type not in ALLOWED_TYPES:
        raise errors.ValidationError(detail="attachment type is not allowed")
    root = Path(base_dir).resolve(strict=True)
    ext = ".png" if media_type == "image/png" else ".jpg"
    name = f"{uuid.uuid4()}{ext}"
    path = (root / name).resolve()
    if not str(path).startswith(str(root)):
        raise errors.ValidationError(detail="invalid attachment path")
    for parent in path.parents:
        if parent == parent.parent:
            break
        if parent.is_symlink():
            raise errors.ValidationError(detail="symlink parent is not allowed")
    with open(path, "wb") as fh:
        fh.write(data)
    return str(path)

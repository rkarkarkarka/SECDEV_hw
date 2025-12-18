from __future__ import annotations

import base64
import hashlib
import hmac
import secrets

from . import errors

_SECRET = secrets.token_bytes(32)
_ITERATIONS = 130_000


def hash_password(password: str) -> str:
    if not password or len(password) < 8:
        raise errors.ValidationError(message="password must be at least 8 chars")
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, _ITERATIONS)
    salt_b64 = base64.b64encode(salt).decode()
    digest_b64 = base64.b64encode(digest).decode()
    return f"pbkdf2${_ITERATIONS}${salt_b64}${digest_b64}"


def verify_password(password: str, hashed: str) -> bool:
    try:
        _, iterations_str, salt_b64, digest_b64 = hashed.split("$")
    except ValueError:
        return False
    salt = base64.b64decode(salt_b64)
    digest = base64.b64decode(digest_b64)
    new_digest = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, int(iterations_str)
    )
    return hmac.compare_digest(digest, new_digest)


def generate_token() -> str:
    return secrets.token_urlsafe(32)


def sign_payload(payload: str) -> str:
    signature = hmac.new(_SECRET, payload.encode("utf-8"), hashlib.sha256).digest()
    return base64.urlsafe_b64encode(signature).decode()


def verify_signature(payload: str, signature: str) -> bool:
    expected = sign_payload(payload)
    return hmac.compare_digest(expected, signature)

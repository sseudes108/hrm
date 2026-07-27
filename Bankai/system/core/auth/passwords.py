"""Hash de senha com PBKDF2-HMAC-SHA256, sem dependência externa."""

import base64
import hashlib
import hmac
import secrets


_ALGORITHM = "sha256"
_ITERATIONS = 310_000


def hash_password(password: str, *, salt: bytes | None = None) -> str:
    if len(password) < 8:
        raise ValueError("A senha deve possuir ao menos 8 caracteres.")
    salt = salt or secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac(_ALGORITHM, password.encode("utf-8"), salt, _ITERATIONS)
    return "$".join(
        ("pbkdf2", _ALGORITHM, str(_ITERATIONS), _encode(salt), _encode(digest))
    )


def verify_password(password: str, stored_hash: str) -> bool:
    try:
        scheme, algorithm, iterations, salt, expected = stored_hash.split("$")
        if scheme != "pbkdf2" or algorithm != _ALGORITHM:
            return False
        digest = hashlib.pbkdf2_hmac(
            algorithm,
            password.encode("utf-8"),
            _decode(salt),
            int(iterations),
        )
        return hmac.compare_digest(_encode(digest), expected)
    except (TypeError, ValueError):
        return False


def _encode(value: bytes) -> str:
    return base64.urlsafe_b64encode(value).decode("ascii").rstrip("=")


def _decode(value: str) -> bytes:
    return base64.urlsafe_b64decode(value + "=" * (-len(value) % 4))

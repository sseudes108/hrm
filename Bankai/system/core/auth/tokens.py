"""Tokens de sessão assinados para cookies não confidenciais."""

import base64
import hashlib
import hmac
import json
import os
import time
from typing import Any


_DEVELOPMENT_SECRET = "zanpakutou-development-cookie-secret-change-in-production"


def issue_token(*, username: str, app_id: str, secret_env: str, lifetime_days: int) -> str:
    payload = {
        "sub": username,
        "app": app_id,
        "exp": int(time.time()) + lifetime_days * 86_400,
    }
    encoded = _encode(json.dumps(payload, separators=(",", ":")).encode("utf-8"))
    signature = _sign(encoded, secret_env)
    return f"{encoded}.{signature}"


def verify_token(token: str | None, *, app_id: str, secret_env: str) -> dict[str, Any] | None:
    if not token or "." not in token:
        return None
    encoded, signature = token.rsplit(".", 1)
    if not hmac.compare_digest(_sign(encoded, secret_env), signature):
        return None
    try:
        payload = json.loads(_decode(encoded))
    except (ValueError, json.JSONDecodeError):
        return None
    if payload.get("app") != app_id or not isinstance(payload.get("sub"), str):
        return None
    if int(payload.get("exp", 0)) < time.time():
        return None
    return payload


def _sign(value: str, secret_env: str) -> str:
    secret = os.getenv(secret_env, _DEVELOPMENT_SECRET)
    return _encode(hmac.new(secret.encode("utf-8"), value.encode("ascii"), hashlib.sha256).digest())


def _encode(value: bytes) -> str:
    return base64.urlsafe_b64encode(value).decode("ascii").rstrip("=")


def _decode(value: str) -> str:
    return base64.urlsafe_b64decode(value + "=" * (-len(value) % 4)).decode("utf-8")

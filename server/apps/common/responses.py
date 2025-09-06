from __future__ import annotations

from typing import Any, Dict


def success_response(data: Any = None, message: str = 'OK', code: int = 0) -> Dict[str, Any]:
    return {
        'code': code,
        'message': message,
        'data': data,
    }


def error_response(message: str, code: int = 1, data: Any = None) -> Dict[str, Any]:
    return {
        'code': code,
        'message': message,
        'data': data,
    }

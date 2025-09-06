from __future__ import annotations

from typing import Any
from rest_framework.renderers import JSONRenderer


class UnifiedJSONRenderer(JSONRenderer):
    """Wrap all responses into {code,message,data} unless already wrapped."""

    def render(self, data: Any, accepted_media_type=None, renderer_context=None):  # type: ignore[override]
        # DRF error responses have 'detail' or 'non_field_errors'
        if isinstance(data, dict) and {'code', 'message', 'data'} <= set(data.keys()):
            wrapped = data
        else:
            status_code = 0
            message = 'OK'
            if isinstance(data, dict):
                if 'detail' in data:  # error case
                    status_code = 1
                    message = str(data.get('detail'))
                    data = data.get('data') or None
            wrapped = {'code': status_code, 'message': message, 'data': data}
        return super().render(wrapped, accepted_media_type, renderer_context)

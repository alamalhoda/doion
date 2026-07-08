import contextvars
import logging
import uuid

from django.utils.deprecation import MiddlewareMixin

_correlation_id: contextvars.ContextVar[str] = contextvars.ContextVar(
    "correlation_id", default=""
)


class CorrelationIdFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.correlation_id = _correlation_id.get()
        return True


class CorrelationIDMiddleware(MiddlewareMixin):
    def process_request(self, request):
        correlation_id = request.headers.get(
            "X-Correlation-ID", str(uuid.uuid4())
        ).strip()
        if not correlation_id:
            correlation_id = str(uuid.uuid4())
        _correlation_id.set(correlation_id)
        request.correlation_id = correlation_id
        return None

    def process_response(self, request, response):
        response["X-Correlation-ID"] = _correlation_id.get()
        return response


def get_correlation_id() -> str:
    return _correlation_id.get()

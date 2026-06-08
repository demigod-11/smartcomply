import time
import uuid

from loguru import logger


class RequestContextMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.request_id = str(uuid.uuid4())
        actor_name = getattr(getattr(request, "actor", None), "name", "-")
        request.log = logger.bind(request_id=request.request_id, actor_name=actor_name)
        start = time.perf_counter()
        response = self.get_response(request)
        duration_ms = (time.perf_counter() - start) * 1000
        request.log.info(
            "request_completed method={} path={} status={} duration_ms={:.2f}",
            request.method,
            request.path,
            response.status_code,
            duration_ms,
        )
        response["X-Request-ID"] = request.request_id
        return response

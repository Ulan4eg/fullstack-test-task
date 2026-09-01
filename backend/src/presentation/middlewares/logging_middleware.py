from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
import time
import json
from ...core.logging import logger

class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware для логирования всех запросов"""

    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        # Логирование запроса
        logger.info(
            f"Request: {request.method} {request.url.path}",
            extra={
                "method": request.method,
                "path": request.url.path,
                "query": str(request.query_params),
                "client": request.client.host if request.client else None,
                "user_agent": request.headers.get("user-agent"),
            }
        )

        # Обработка запроса
        try:
            response = await call_next(request)

            # Логирование ответа
            process_time = time.time() - start_time
            logger.info(
                f"Response: {response.status_code} - {process_time:.3f}s",
                extra={
                    "status_code": response.status_code,
                    "process_time": process_time,
                }
            )

            return response

        except Exception as e:
            logger.error(
                f"Error processing request: {str(e)}",
                extra={
                    "error": str(e),
                    "error_type": type(e).__name__,
                }
            )
            raise
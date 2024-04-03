from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import FastAPI
import time
from fastapi import Response, Request
from typing import Callable
from customlog import custom_logger

class RouterLoggingMiddleware(BaseHTTPMiddleware):
    def __init__(self, *, app: FastAPI):
        self._logger = custom_logger
        super().__init__(app)

    async def dispatch(
            self, 
            request: Request, 
            call_next: Callable
            ):
        path = request.url.path
        body = await request.body()
        # for i in request.body:
        #     body.append(i)
        if query := request.query_params:
            path += '?'
            for key, val in query.items():
                path += key
                path += '='+val+'&'
        
        request_dict = {
            'path': path,
            'method': request.method,
            'ip': request.client.host,
            'body': body,
        }
        response = None
        try:
            start = time.perf_counter()
            response = await call_next(request)
            result = time.perf_counter() - start
        except Exception as exp:
            status = self._logger.exception({
                'status': request.method,
                'path': request.url.path,
                'details': exp
            })
        else:
            response_dict = {
                'status': response.status_code,
                'perf_time': result,
            }
            log_dict = {
                'response': response_dict,
                'request': request_dict,
            }
            self._logger.info(log_dict)

            return response
            
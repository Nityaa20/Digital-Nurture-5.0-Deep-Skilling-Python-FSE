from typing import Any, Optional

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse


# URL versioning (/api/v1/) is simple and visible in every request.
# Header versioning (Accept: application/vnd.api+json;version=1) keeps URLs clean
# but is harder to test in a browser and requires clients to set custom headers.


def error_response(code: str, message: str, field: Optional[str] = None, status_code: int = 400):
    return JSONResponse(
        status_code=status_code,
        content={'error': {'code': code, 'message': message, 'field': field}},
    )


def not_found(resource: str, resource_id: int):
    return error_response(
        'NOT_FOUND',
        f'{resource} with id {resource_id} does not exist',
        status_code=404,
    )


def paginate(query_result, total: int, page: int, page_size: int, request: Request, path: str):
    base = str(request.base_url).rstrip('/')
    next_url = None
    previous_url = None
    if page * page_size < total:
        next_url = f'{base}{path}?page={page + 1}&page_size={page_size}'
    if page > 1:
        previous_url = f'{base}{path}?page={page - 1}&page_size={page_size}'
    return {
        'count': total,
        'next': next_url,
        'previous': previous_url,
        'results': query_result,
    }


async def http_exception_handler(request: Request, exc: HTTPException):
    code_map = {404: 'NOT_FOUND', 400: 'BAD_REQUEST', 401: 'UNAUTHORIZED', 422: 'VALIDATION_ERROR'}
    return error_response(
        code_map.get(exc.status_code, 'ERROR'),
        str(exc.detail),
        status_code=exc.status_code,
    )

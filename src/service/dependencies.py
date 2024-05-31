from fastapi import Header, Request
import datetime
import logging
import contextvars
from service.logger import LoggerAdapter

logger = LoggerAdapter(logging.getLogger(__name__), None)


class HeaderParams:
    """Class holding the custom header details"""

    def __init__(
            self,
            request_id: str = Header(..., min_length=1, max_length=20),
            request_timestamp: datetime.datetime = Header(...)
    ):
        self.request_id = request_id
        self.request_timestamp = request_timestamp


class LogInboundRequest:
    """Class for logging the inbound request"""

    def __init__(self, ctx: contextvars.ContextVar):
        self.ctx = ctx

    async def __call__(self, request: Request):
        log_fields = {"path": request.scope['path']}

        rb = await request.body()
        if len(rb) > 0:
            request_body = await request.json()
            message = request_body["data"]
            log_fields["body"] = request_body
        if len(request.query_params) > 0:
            query_list = []
            for i in request.query_params.multi_items():
                query_list.append({i[0]: i[1]})
            log_fields["query"] = query_list

        logger.info(ctx=self.ctx, msg="Incoming Request Received", extra_fields={"request_payload": {"message" : message}})

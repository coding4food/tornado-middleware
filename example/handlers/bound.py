import json

from marshmallow import Schema, fields

from abstractions import HTTPResponse
from handlers.bind_request import bind_arguments, Json, Header


class RequestFiltersSchema(Schema):
    account_id = fields.Int(required=True)


class RequestSchema(Schema):
    filters = fields.Nested(RequestFiltersSchema, required=True)
    institution_id = fields.List(fields.Int(required=True), required=True)
    message_id = fields.Str(allow_none=False)


@bind_arguments
async def bound(request, data: RequestSchema, js: Json, message_id: Header('X-Request-Id')):
    print('request', request)
    print('data', data)
    print('json', js)
    print('message_id', message_id)

    return HTTPResponse(
        status_code=200,
        headers={'Contetnt-Type': 'application/json', 'Foo': message_id},
        body=json.dumps(data).encode()
    )

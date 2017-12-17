from flask import request
from marshmallow import Schema, post_dump
from marshmallow.fields import Nested, String, Boolean
from marshmallow.validate import Email, Length

from aleph.core import url_for
from aleph.serializers.common import BaseSchema
from aleph.model import Role


class RoleSchema(BaseSchema):
    name = String(validate=Length(min=3))
    email = String(validate=Email())
    api_key = String(dump_only=True)
    type = String(dump_only=True)
    # foreign_id = String(dump_only=True)
    # is_admin = Boolean(dump_only=True)

    @post_dump
    def transient(self, data):
        data['uri'] = url_for('roles_api.view', id=data.get('id'))
        data['writeable'] = str(request.authz.id) == str(data.get('id'))
        if not data['writeable']:
            data.pop('api_key')
            data.pop('email')
        return data


class RoleCodeCreateSchema(Schema):
    email = String(validate=Email(), required=True)


class RoleCreateSchema(Schema):
    name = String()
    password = String(validate=Length(min=Role.PASSWORD_MIN_LENGTH),
                      required=True)
    code = String(required=True)


class RoleReferenceSchema(RoleSchema):
    id = String(required=True)


class LoginSchema(Schema):
    email = String(validate=Email(), required=True)
    password = String(validate=Length(min=3))


class PermissionSchema(BaseSchema):
    write = Boolean(required=True)
    read = Boolean(required=True)
    collection_id = String(dump_only=True, required=True)
    role = Nested(RoleReferenceSchema)

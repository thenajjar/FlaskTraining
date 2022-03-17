from marshmallow import Schema, fields


class RegisterUserRequestSchema(Schema):
    username = fields.Str(default='username')
    name = fields.Str(default='FirstName LastName')
    email = fields.Str(default='email@domain.com')
    phone = fields.Str(default='phone')
    password = fields.Str(default='password')
    confirm_password = fields.Str(default='confirm_password')


class RegisterUserResponseSchema(Schema):
    user_id = fields.Str(default='1')


class GetUserResponseSchema(Schema):
    user_id = fields.Str(default='1')
    username = fields.Str(default='username')
    name = fields.Str(default='FirstName LastName')
    email = fields.Str(default='email@domain.com')
    phone = fields.Str(default='+966541942414')


class GetUserRequestSchema(Schema):
    user_id = fields.Str(default='1')


class OTPResponseSchema(Schema):
    user_id = fields.Str(default='1')
    username = fields.Str(default='username')
    name = fields.Str(default='FirstName LastName')
    email = fields.Str(default='email@domain.com')
    phone = fields.Str(default='+966541942414')


class OTPRequestSchema(Schema):
    user_id = fields.Str(default='1')


class OTPSchema(Schema):
    message = fields.Str(default='Success')

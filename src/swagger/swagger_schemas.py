from marshmallow import Schema, fields


default_user_id = 'id'
default_username = 'username'
default_name = 'FirstName LastName'
default_email = 'email@domain.com'
default_phone = '+<country code><phone number>'


class RegisterUserRequestSchema(Schema):
    username = fields.Str(default=default_username)
    name = fields.Str(default=default_name)
    email = fields.Str(default=default_email)
    phone = fields.Str(default=default_phone)
    password = fields.Str(default='password')
    confirm_password = fields.Str(default='confirm_password')


class RegisterUserResponseSchema(Schema):
    user_id = fields.Str(default=default_user_id)


class GetUserResponseSchema(Schema):
    user_id = fields.Str(default=default_user_id)
    username = fields.Str(default=default_username)
    name = fields.Str(default=default_name)
    email = fields.Str(default=default_email)
    phone = fields.Str(default=default_phone)


class GetUserRequestSchema(Schema):
    user_id = fields.Str(default=default_user_id)


class OTPResponseSchema(Schema):
    user_id = fields.Str(default=default_user_id)
    username = fields.Str(default=default_username)
    name = fields.Str(default=default_name)
    email = fields.Str(default=default_email)
    phone = fields.Str(default=default_phone)


class OTPRequestSchema(Schema):
    user_id = fields.Str(default=default_user_id)


class OTPSchema(Schema):
    message = fields.Str(default='Success')

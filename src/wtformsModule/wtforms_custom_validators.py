from wtforms.validators import ValidationError
from src.sqlalchemyModule.users import UsersDb


class UniqueValue(object):
    """WTform validation object that takes a wtform field value and raises error if the field value exists 
    in a column, identified by the wtform field id, in the users' table in the flask database
    """

    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        field_id = field.id
        if not self.message:
            self.message = 'The {} already exists'.format(field_id)
        value = UsersDb.query.filter(getattr(UsersDb, field_id).like("%%%s%%" % field.data)).first()
        if value:
            raise ValidationError(self.message)


class ValueExists(object):
    """WTform validation object that takes a wtform field value and raises error if the field value does not exist
    in a column, identified by the wtform field id, in the users' table in the flask database
    """

    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        field_id = field.id
        if not self.message:
            self.message = 'The {} does not exists'.format(field_id)
        value = UsersDb.query.filter(getattr(UsersDb, field_id).like("%%%s%%" % field.data)).first()
        if not value:
            raise ValidationError(self.message)


class PasswordFormat(object):
    """WTform validation object that takes a wtform field value and raises an error if the value does not fulfill
    password requirements of containing a symbol @#!$&, cap letter, small letter, and a number
    """

    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        if not self.message:
            self.message = 'Password error'
        password = field.data
        special_char = ["@", "#", "!", "$", "&"]
        if len(password) < 6:
            self.message = 'length should be at least 6'
        error = False

        if len(password) > 20:
            self.message = 'length should be not be greater than 8'
            error = True

        elif not any(char.isdigit() for char in password):
            self.message = 'Password should have at least one numeral'
            error = True

        elif not any(char.isupper() for char in password):
            self.message = 'Password should have at least one uppercase letter'
            error = True

        elif not any(char.islower() for char in password):
            self.message = 'Password should have at least one lowercase letter'
            error = True

        elif not any(char in special_char for char in password):
            self.message = 'Password should have at least one of the symbols @#!$&'
            error = True

        if error:
            raise ValidationError(self.message)


class IsRole(object):
    """WTform validation object that takes a wtform field value and raises error if the field value is not a valid role
    """

    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        field_id = field.id
        if not self.message:
            self.message = 'The role {} is not valid.'.format(field_id)
        if str(field.data).lower() not in ["user", "admin"]:
            raise ValidationError(self.message)

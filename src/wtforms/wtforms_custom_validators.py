from wtforms.validators import ValidationError
from src.database.users import users_db


class unique_value(object):
    """WTform validation object that takes a wtform field value and raises error if the field value exists 
    in a column, identfied by the wtform field id, in the users table in the flask database
    """

    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        field_id = field.id
        if not self.message:
            self.message = 'The {} already exists'.format(field_id)
        if users_db.exists(field_id, field.data):
            raise ValidationError(self.message)


class exists(object):
    """WTform validation object that takes a wtform field value and raises error if the field value does not exists 
    in a column, identfied by the wtform field id, in the users table in the flask database
    """

    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        field_id = field.id
        if not self.message:
            self.message = 'The {} already exists'.format(field_id)
        if not users_db.exists(field_id, field.data):
            raise ValidationError(self.message)


class password_format(object):
    """WTform validation object that takes a wtform field value and raises an error if the value does not fulfill
    password requirments of containting a symbol @#!$&, cap letter, small letter, and a number
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

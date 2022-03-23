from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Email, Length

from src.wtforms.wtforms_custom_validators import UniqueValue, PasswordFormat, ValueExists


class RegisterNewUserForm(FlaskForm):
    class Meta:
        csrf = False

    username = StringField('username', validators=[
        DataRequired(), Length(min=4, max=16), UniqueValue()])
    name = StringField('name', validators=[
        DataRequired(message="name is required")])
    email = StringField('email', validators=[DataRequired(
        message="email is required"), Email(message="Wrong Email formatting"), UniqueValue()])
    phone = StringField('phone', validators=[DataRequired(
        message="phone is required")])
    password = StringField('password', validators=[DataRequired(
        message="password is required"), PasswordFormat()])
    confirm_password = StringField('confirm_password', validators=[
        DataRequired(message="password is required")])


class GetUserDataForm(FlaskForm):
    class Meta:
        csrf = False

    user_id = StringField('user_id', validators=[DataRequired()])


class OTPVerifyForm(FlaskForm):
    class Meta:
        csrf = False

    user_id = StringField('user_id', validators=[DataRequired()])
    otp = StringField('otp', validators=[DataRequired()])


class LoginForm(FlaskForm):
    class Meta:
        csrf = False

    username = StringField('username', validators=[DataRequired(), ValueExists()])
    password = StringField('password', validators=[DataRequired()])

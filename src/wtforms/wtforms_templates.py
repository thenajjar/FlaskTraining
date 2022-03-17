from src.wtforms.wtforms_custom_validators import *

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Email, Length


class RegisterNewUserForm(FlaskForm):
    class Meta:
        csrf = False
    username = StringField('username', validators=[
                           DataRequired(), Length(min=4, max=16), unique_value()])
    name = StringField('name', validators=[
                       DataRequired(message="name is requiered")])
    email = StringField('email', validators=[DataRequired(
        message="email is requiered"), Email(message="Wrong Email formatting"), unique_value()])
    phone = StringField('phone', validators=[DataRequired(
        message="phone is requiered"), unique_value()])
    password = StringField('password', validators=[DataRequired(
        message="password is requiered"), password_format()])
    confirm_password = StringField('confirm_password', validators=[
                                   DataRequired(message="password is requiered")])


class GetUserDataForm(FlaskForm):
    class Meta:
        csrf = False
    user_id = StringField('user_id', validators=[DataRequired()])


class OTPVerifyForm(FlaskForm):
    class Meta:
        csrf = False
    user_id = StringField('user_id', validators=[DataRequired()])
    otp = StringField('otp', validators=[DataRequired()])

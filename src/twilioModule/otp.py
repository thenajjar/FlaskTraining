from twilio.rest import Client

from src.celeryModule.celery_config import celery
from src.dotenvModule.load import get_var

account_sid = str(get_var('TWILIO_ACCOUNT_SID'))
auth_token = str(get_var('TWILIO_AUTH_TOKEN'))
app_token = str(get_var('TWILIO_VERIFY_APP_TOKEN'))


def send_otp_sms_call(phone):
    send_otp_sms.apply_async(args=[phone, account_sid, auth_token, app_token])


@celery.task
def send_otp_sms(phone, twilio_account_sid, twilio_auth_token, twilio_app_token):
    try:
        client = Client(twilio_account_sid, twilio_auth_token)
        client.verify \
            .services(twilio_app_token) \
            .verifications \
            .create(to=phone, channel='sms')
    except Exception as error_message:
        raise Exception("500", "SERVER_FAILURE",
                        "Server failed to send OTP message.", error_message)


def verify_otp_sms(phone, code):
    try:
        client = Client(account_sid, auth_token)
        verification_check = client.verify \
            .services(app_token) \
            .verification_checks \
            .create(to=phone, code=code)
        if verification_check.status == "approved":
            return True
    except Exception as error_message:
        raise Exception("500", "SERVER_FAILURE",
                        "Server failed to verify OTP message.", error_message)

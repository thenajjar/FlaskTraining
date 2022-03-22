from src.dotenv.load import get_var

from twilio.rest import Client

account_sid = get_var('TWILIO_ACCOUNT_SID')
auth_token = get_var('TWILIO_AUTH_TOKEN')
app_token = get_var('TWILIO_VERIFY_APP_TOKEN')

client = Client(account_sid, auth_token)


def send_otp_sms(phone):
    try:
        verification = client.verify \
            .services(app_token) \
            .verifications \
            .create(to=phone, channel='sms')
        return(verification.sid)
    except Exception as error_message:
        raise Exception("500", "SERVER_FAILURE", "Server failed to send OTP message.", error_message)


def verify_otp_sms(phone, code):
    try:
        verification_check = client.verify \
            .services(app_token) \
            .verification_checks \
            .create(to=phone, code=code)
        if verification_check.status == "approved":
            return True
    except Exception as error_message:
        raise Exception("500", "SERVER_FAILURE" ,"Server failed to veirfy OTP message.", error_message)

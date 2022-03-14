from twilio.rest import Client
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
app_token = os.getenv('TWILIO_VERIFY_APP_TOKEN')

client = Client(account_sid, auth_token)
try:
    verification = client.verify \
        .services(app_token) \
        .verifications \
        .create(to='+966541942414', channel='sms')
    print(verification.sid)
except Exception as error_message:
    print(error_message)
    
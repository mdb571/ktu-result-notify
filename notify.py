from twilio.rest import Client
from twilio import twiml
import os
from dotenv import load_dotenv

load_dotenv()

ACCOUNT_SID =os.environ['ACCOUNT_SID']
AUTH_TOKEN = os.environ['AUTH_TOKEN']

client = Client(ACCOUNT_SID,AUTH_TOKEN)

result_url=os.environ.get('DEPLOY_URL')+'/results/'+os.environ.get('KTU_ID')

def send_notification():
    message = client.messages.create(
            body="Hey your KTU results just got published. Here is your result \n "+result_url+'.pdf',
            from_=os.environ.get('TWILIO_NO'),  # add your twilio no. here
            to=os.environ.get('MY_NUM')  # add your verified number here
        )

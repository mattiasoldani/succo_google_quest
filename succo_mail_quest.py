# https://developers.google.com/gmail/api/quickstart/python
# https://developers.google.com/gmail/api/guides/drafts
# https://developers.google.com/gmail/api/guides/sending
# https://developers.google.com/gmail/api/guides/uploads
# https://stackoverflow.com/questions/40186856/403-request-had-insufficient-authentication-scopes-when-creating-drafts-in-goo

# required imports
from __future__ import print_function
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from apiclient import errors
import pandas as pd
import time
import os
import mimetypes
import base64

######################
# starting chronometer
tStart = time.time()
print("quest started!")

# settings
mail_from = "youremail@gmail.com"  # sender mail
b_attachment = False  # are there any attachments?
b_draft = True  # if True (False) emails are uploaded as drafts (are sent directly)

print("%s mode selected" % ("draft" if b_draft else "send"))

# setup the API w/ the authorisation & build service
SCOPES = ["https://mail.google.com/"]
creds = None
if os.path.exists('tokens/mail/token.json'):
    creds = Credentials.from_authorized_user_file('tokens/mail/token.json', SCOPES)
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'keys/client_secret.json', SCOPES)
        creds = flow.run_local_server(port=0)
    with open('tokens/mail/token.json', 'w') as token:
        token.write(creds.to_json())
service = build('gmail', 'v1', credentials=creds)

# load input file
# CSV file with list of emails to create
# format per line i.e. per email: recipient, recipient in CC, attachment file (path+name, useless if no attachments), another fields with customised information for each email
# notes:
# - the file entries have to be separated by semicolon
# - in case of multiple recipients (or CC) put them after one another, separated by commas (with no spaces)
indata = pd.read_csv("input/mail_recipientList.csv", delimiter=";", names=["ls_rec", "ls_cc", "ls_att_path", "ls_att_name", "ls_info"])

for i, mail_rec in enumerate(indata.ls_rec):

    # unpack variables
    mail_cc = indata.ls_cc[i]
    mail_att_path = indata.ls_att_path[i]
    mail_att_name = indata.ls_att_name[i]
    mail_custom_info = indata.ls_info[i]

    #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
    # set subject
    mail_subject = \
    "test message"
    
    # set message
    mail_text = \
    "Good morning,\n\nthis is a test message.\n\nCheers,\n\nsucco"
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    # create the messages
    message = MIMEMultipart()
    message['from'] = mail_from
    message['to'] = mail_rec
    message['cc'] = mail_cc    
    message['subject'] = mail_subject
    message.attach(MIMEText(mail_text))
    if b_attachment:
        with open(mail_att_path+mail_att_name,'rb') as file:
            message.attach(MIMEApplication(file.read(), Name=mail_att_name))
    message_final = {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}

    # upload them to drafts, or...
    if b_draft:
        service.users().drafts().create(userId=mail_from, body={'message': message_final}).execute()
        print("draft %d created -- to %s" % (i, mail_rec))
    
    # ... send them directly
    else:
        service.users().messages().send(userId=mail_from, body=message_final).execute()
        print("message %d sent -- to %s -- now waiting for 10 s" % (i, mail_rec))
        time.sleep(10)
    
###############################################
# stopping chronometer & printing final results
tStop = time.time()
print("quest completed! in %f s" % (tStop-tStart))
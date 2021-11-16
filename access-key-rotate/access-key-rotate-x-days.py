import datetime, boto3, os, json
from botocore.exceptions import ClientError
from datetime import datetime, timezone
import json
import smtplib

globalVars  = {}
globalVars['Region_Name'] = "ap-south-1"

def get_usr_old_keys(event, context):

    client = boto3.client('iam',region_name = globalVars['Region_Name'])
    paginator = client.get_paginator('list_users')
    CurrentDate = datetime.now(timezone.utc)
    MaxKeyAge = 30

    for response in paginator.paginate():
        for user in response['Users']:
            user_name = user['UserName']
            list_key = client.list_access_keys(UserName = user_name)
            for access_key in list_key['AccessKeyMetadata']:
                access_key_id = access_key['AccessKeyId']
                key_creation_date = access_key['CreateDate']
                age = (CurrentDate - key_creation_date).days
                if age > MaxKeyAge:
                    print("Access key Expired for : ", user_name)
                    gmail_user = <e-mail>
                    gmail_password = <Password>
                    sent_from = <e-mail>
                    sent_to = <e-mail>
                    sent_sub = "Access key Expired!!"
                    sent_body = "Dear User -  Your Aceess key Expired. Please create new one."
                    try:
                        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                        server.ehlo()
                        server.login(gmail_user, gmail_password)
                        server.sendmail(sent_from, sent_to, sent_body)
                        #server.close()
                        print(email_text)
                        print('Email sent!')
                    except Exception as exception:
                        print("Error: %s!\n\n" % exception)

                    
def lambda_handler(event, context):
    get_usr_old_keys(event,context)

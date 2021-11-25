import datetime, boto3, os, json
from botocore.exceptions import ClientError
from datetime import datetime, timezone
import json
import smtplib

globalVars  = {}
globalVars['Region_Name'] = "ap-south-1"

def get_usr_old_keys(event, context):

    client = boto3.client('iam',region_name = globalVars['Region_Name'])
    #snsClient = boto3.client('sns',region_name = globalVars['Region_Name'])
    #ses = boto3.client('ses')
    paginator = client.get_paginator('list_users')
    CurrentDate = datetime.now(timezone.utc)
    MaxKeyAge = 30
    sec_client = boto3.client('secretsmanager')
    response1 = sec_client.get_secret_value(SecretId='lambda/AccessKeyRotate/password')
    sec_dict = json.loads(response1['SecretString'])
    sec_email = sec_dict['Email']
    sec_password = sec_dict['Password']
    
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
                    gmail_user = sec_email
                    sent_from = sec_email
                    sent_to = user_name
                    sent_sub = "Access key Expired!!"
                    sent_body = "Dear User -  Your Access key Expired. Please create new one."
                    try:
                        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                        server.ehlo()
                        server.login(gmail_user, sec_password)
                        server.sendmail(sent_from, sent_to, sent_body)
                        server.close()
                        print('Email sent!')
                    except Exception as exception:
                        print("Error: %s!\n\n" % exception)
                    
def lambda_handler(event, context):
    get_usr_old_keys(event,context)

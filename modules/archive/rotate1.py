import boto3
from datetime import datetime, timedelta
import json
import csv
import time

def lambda_handler(event, context):
    client = boto3.client('iam')
    ses = boto3.client('ses')
    
    # Calculate the inactive cutoff date
    inactive_cutoff = datetime.now() - timedelta(days=90)
    
    # Get all IAM users
    response = client.list_users()
    
    # Create a dictionary to store inactive users' data
    inactive_users = {}
    
    # Loop through each user
    for user in response['Users']:
        username = user['UserName']
        
        # Check if the user has ever logged in
        if 'PasswordLastUsed' not in user:
            last_sign_in = None
        else:
            last_sign_in = user['PasswordLastUsed']
        
        # If the user has never logged in or has been inactive for more than 90 days, add them to the inactive_users dictionary
        if last_sign_in is None or last_sign_in < inactive_cutoff:
            inactive_users[username] = last_sign_in
    
    # Wait for 14 days before disabling the inactive users
    time.sleep(1209600)
    
    # Disable the inactive users
    for username in inactive_users:
        client.update_user(
            UserName=username,
            PasswordExpirationTime=datetime.now()
        )
        
        # Send an email to notify the user that their account has been disabled
        message = "Your IAM account has been disabled due to inactivity."
        subject = "IAM Account Disabled"
        sender = "sender@example.com"
        recipient = username
        ses.send_email(
            Source=sender,
            Destination={
                'ToAddresses': [
                    recipient
                ]
            },
            Message={
                'Subject': {
                    'Data': subject
                },
                'Body': {
                    'Text': {
                        'Data': message
                    }
                }
            }
        )
        
    # Convert the inactive_users dictionary to a CSV file
    csv_buffer = csv.writer(io.StringIO())
    csv_buffer.writerow(['username', 'last_console_sign_in'])
    for username, last_sign_in in inactive_users.items():
        csv_buffer.writerow([username, last_sign_in])
    
    # Send the CSV file as an email attachment
    attachment = csv_buffer.getvalue()
    message = "Please find attached a list of inactive IAM users."
    subject = "Inactive IAM Users Report"
    sender = "sender@example.com"
    recipient = "recipient@example.com"
    ses.send_email(
        Source=sender,
        Destination={
            'ToAddresses': [
                recipient
            ]
        },
        Message={
            'Subject': {
                'Data': subject
            },
            'Body': {
                'Text': {
                    'Data': message
                }
            }
        },
        Attachments=[
            {
                'Filename': 'inactive_users.csv',
                'Content': attachment
            }
        ]
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps('Inactive user check completed')
    }




{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AllowEncryptDecryptSpecificKey",
            "Effect": "Allow",
            "Action": [
                "kms:Encrypt",
                "kms:Decrypt"
            ],
            "Resource": "arn:aws:kms:us-east-1:678564198086:key/74506a64-1d06-4fce-8198-eddd8be037e4"
        }
    ]
}


{
  "Version": "2012-10-17",
  "Statement": {
    "Effect": "Allow",
    "Action": [
      "kms:DescribeKey",
      "kms:GenerateDataKey",
      "kms:Decrypt"
    ],
    "Resource": [
      "arn:aws:kms:us-west-2:111122223333:key/1234abcd-12ab-34cd-56ef-1234567890ab",
      "arn:aws:kms:us-west-2:111122223333:key/0987dcba-09fe-87dc-65ba-ab0987654321"
    ]
  }
}




#deny getobject or put object if ipaddrews is wrong

{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "DenyGetObjectUnlessSpecificIP",
            "Effect": "Deny",
            "Principal": "*",
            "Action": [
                "s3:GetObject",
                "s3:PutObject"
            ],
            "Resource": "arn:aws:s3:::s3-testing-testingw/*",
            "Condition": {
                "NotIpAddress": {
                    "aws:SourceIp": "165.225.216.165"
                }
            }
        }
    ]
}

# DenyAccessToDocumentFolder
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "DenyAccessToDocumentFolder",
      "Effect": "Deny",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::s3-testing-testingw/Document/*",
      "Condition": {
        "NotIpAddress": {
          "aws:SourceIp": "123.123.123.123/32"
        }
      }
    }
  ]
}


{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "DenyAccessToDocumentFolders",
      "Effect": "Deny",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": [
        "arn:aws:s3:::s3-testing-testingw/Document/*",
        "arn:aws:s3:::s3-testing-testingw/Document1/*"
      ],
      "Condition": {
        "NotIpAddress": {
          "aws:SourceIp": "123.123.123.123/32"
        }
      }
    }
  ]
}

#DenyAccessToDocumentFolders
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "DenyAccessToDocumentFolders",
      "Effect": "Deny",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": [
        "arn:aws:s3:::s3-testing-testingw/Document/*",
        "arn:aws:s3:::s3-testing-testingw/Document1/*"
      ],
      "Condition": {
        "NotIpAddress": {
          "aws:SourceIp": "123.123.123.123/32"
        }
      }
    }
  ]
}

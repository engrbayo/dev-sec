import os
import boto3

IAM_INSTANCE_PROFILE_ARN = os.environ['IAM_INSTANCE_PROFILE_ARN']

def lambda_handler(event, context):
    ec2_client = boto3.client('ec2')
    
    # Retrieve all EC2 instances
    response = ec2_client.describe_instances()
    
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            
            # Check if an IAM role is already attached
            if 'IamInstanceProfile' in instance:
                print(f"Instance {instance_id} already has an IAM role attached. Skipping...")
                continue
            
            # Attach IAM role to the instance
            try:
                response = ec2_client.associate_iam_instance_profile(
                    IamInstanceProfile={
                        'Arn': IAM_INSTANCE_PROFILE_ARN
                    },
                    InstanceId=instance_id
                )
                print(f"IAM role attached to instance {instance_id}.")
                
            except Exception as e:
                print(f"Error attaching IAM role to instance {instance_id}: {str(e)}")
    
    return {
        'statusCode': 200,
        'body': 'IAM role attachment process completed.'
    }

import os
import boto3

IAM_INSTANCE_PROFILE_ARN = os.environ['IAM_INSTANCE_PROFILE_ARN']
SSM_MANAGED_POLICY_ARN = os.environ['SSM_MANAGED_POLICY_ARN']

def has_policy_attached(iam_client, role_name, policy_arn):
    try:
        response = iam_client.list_attached_role_policies(RoleName=role_name)
        for policy in response['AttachedPolicies']:
            if policy['PolicyArn'] == policy_arn:
                return True
        return False
    except Exception as e:
        print(f"Error checking attached policies for IAM role {role_name}: {str(e)}")
        return False

def lambda_handler(event, context):
    ec2_client = boto3.client('ec2')
    iam_client = boto3.client('iam')
    
    # Retrieve all EC2 instances
    response = ec2_client.describe_instances()
    
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            
            # Check if an IAM role is already attached
            if 'IamInstanceProfile' in instance:
                instance_profile_arn = instance['IamInstanceProfile']['Arn']
                instance_profile_name = instance_profile_arn.split('/')[-1]
                
                # Check if IAM role has the desired policy attached
                if not has_policy_attached(iam_client, instance_profile_name, SSM_MANAGED_POLICY_ARN):
                    try:
                        # Attach the desired policy to the IAM role
                        response = iam_client.attach_role_policy(
                            PolicyArn=SSM_MANAGED_POLICY_ARN,
                            RoleName=instance_profile_name
                        )
                        print(f"Desired policy attached to IAM role {instance_profile_name}.")

                    except Exception as e:
                        print(f"Error attaching desired policy to IAM role {instance_profile_name}: {str(e)}")
            
            else:
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

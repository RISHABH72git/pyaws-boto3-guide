import boto3
from botocore.exceptions import ClientError

iam = boto3.client('iam')

if __name__ == '__main__':
    #if user exist in aws
    username = 'demo'
    try:
        response = iam.create_access_key(UserName=username)
        access_key = response['AccessKey']
        print("Access key created successfully!")
        print("Access Key ID:     ", access_key['AccessKeyId'])
        print("Secret Access Key: ", access_key['SecretAccessKey'])
        print("Status:            ", access_key['Status'])
        print("Created On:        ", access_key['CreateDate'])
    except ClientError as e:
        print("Error:", e.response['Error']['Message'])

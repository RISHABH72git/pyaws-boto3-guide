import boto3
iam = boto3.client('iam')

def list_users():
    paginator = iam.get_paginator('list_users')
    for page in paginator.paginate():
        for user in page['Users']:
            print(f"Username       : {user['UserName']}")
            print(f"User ARN       : {user['Arn']}")
            print(f"Created On     : {user['CreateDate']}")
            access_keys = iam.list_access_keys(UserName=user['UserName'])['AccessKeyMetadata']
            for key in access_keys:
                print(f"  AccessKeyId  : {key['AccessKeyId']}")
                print(f"  Status       : {key['Status']}")
                print(f"  Created On   : {key['CreateDate']}")
                last_used = iam.get_access_key_last_used(AccessKeyId=key['AccessKeyId'])
                print(f"  Last Used On : {last_used['AccessKeyLastUsed'].get('LastUsedDate', 'Never')}")
            print("-" * 40)

if __name__ == '__main__':
    list_users()

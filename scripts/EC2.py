import boto3

ec2 = boto3.client('ec2', 'us-east-1')


def list_instances():
    response = ec2.describe_instances()

    instances = []
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            print(instance)
            instance_id = instance['InstanceId']
            state = instance['State']['Name']
            instance_type = instance['InstanceType']
            public_ip = instance.get('PublicIpAddress', 'N/A')
            name_tag = next(
                (tag['Value'] for tag in instance.get('Tags', []) if tag['Key'] == 'Name'),
                'No Name'
            )

            instances.append({
                'InstanceId': instance_id,
                'Name': name_tag,
                'State': state,
                'Type': instance_type,
                'PublicIP': public_ip
            })

    return instances


if __name__ == "__main__":
    ec2_list = list_instances()
    print("✅ EC2 Instances:\n")
    for inst in ec2_list:
        print(f"{inst['InstanceId']} | {inst['Name']} | {inst['State']} | {inst['Type']} | {inst['PublicIP']}")

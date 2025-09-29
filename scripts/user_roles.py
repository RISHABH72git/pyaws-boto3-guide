import boto3

iam = boto3.client('iam')
user_name = "test"  #demo iam user

attached = iam.list_attached_user_policies(UserName=user_name)
print("Attached User Policies:")
for p in attached['AttachedPolicies']:
    policy_name = p['PolicyArn']
    print(f" - {p['PolicyName']}")

# Get inline policies
inline = iam.list_user_policies(UserName=user_name)
print("\nInline Policies:")
for p in inline['PolicyNames']:
    print(f" - {p}")

# Get groups and their policies
groups = iam.list_groups_for_user(UserName=user_name)
print("\nGroup Policies:")
for g in groups['Groups']:
    group_name = g['GroupName']
    print(f"Group: {group_name}")
    group_policies = iam.list_attached_group_policies(GroupName=group_name)
    for gp in group_policies['AttachedPolicies']:
        print(f" - {gp['PolicyName']} (from group)")

import boto3
from botocore.exceptions import ClientError


def get_identity_store_id(region_name=None):
    """
    Fetches the IdentityStoreId from the AWS SSO instance(s).
    """
    sso_admin = boto3.client("sso-admin", region_name=region_name)
    try:
        resp = sso_admin.list_instances()
    except ClientError as e:
        raise RuntimeError(f"Failed to list SSO instances: {e}")
    instances = resp.get("Instances", [])
    if not instances:
        raise RuntimeError("No AWS SSO instances found in this account/region.")
    # If multiple, pick the first; adjust logic if you need a specific one.
    identity_store_id = instances[0].get("IdentityStoreId")
    if not identity_store_id:
        raise RuntimeError("IdentityStoreId not found in the SSO instance.")
    return identity_store_id


def list_all_identity_center_users(region_name=None):
    identity_store_id = get_identity_store_id(region_name=region_name)
    identitystore = boto3.client("identitystore", region_name=region_name)
    users = []
    try:
        paginator = identitystore.get_paginator("list_users")
        page_iterator = paginator.paginate(IdentityStoreId=identity_store_id)
        for page in page_iterator:
            users.extend(page.get("Users", []))
    except ClientError as e:
        raise RuntimeError(f"Failed to list users: {e}")
    return users


def main():
    region = None
    try:
        users = list_all_identity_center_users(region_name=region)
    except Exception as e:
        print(f"Error: {e}")
        return

    if not users:
        print("No users found in Identity Center.")
        return

    for user in users:
        user_id = user.get("UserId")
        user_name = user.get("UserName")
        display_name = user.get("DisplayName", "")
        emails = user.get("Emails", [])
        email = emails[0].get("Value") if emails else ""
        print(f"- {user_name} (ID: {user_id}) DisplayName: {display_name} Email: {email}")


if __name__ == "__main__":
    main()

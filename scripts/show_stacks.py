import boto3
import botocore
import logging
from datetime import datetime
from botocore.config import Config

# Optional: configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

def format_dt(dt):
    if not dt:
        return "N/A"
    if isinstance(dt, datetime):
        return dt.strftime("%Y-%m-%d %H:%M:%S %Z") if dt.tzinfo else dt.strftime("%Y-%m-%d %H:%M:%S")
    return str(dt)

def safe_get(d: dict, key, default=None):
    return d.get(key, default) if isinstance(d, dict) else default

def list_all_stacks(region_name="us-east-1", profile_name=None):
    """
    Lists all CloudFormation stacks in the given region with their details.
    """
    session_kwargs = {}
    if profile_name:
        session_kwargs["profile_name"] = profile_name

    session = boto3.Session(**session_kwargs)
    cfg = Config(retries={"max_attempts": 5, "mode": "standard"})
    client = session.client("cloudformation", region_name=region_name, config=cfg)

    paginator = client.get_paginator("describe_stacks")

    try:
        for page in paginator.paginate():
            stacks = page.get("Stacks", [])
            for stack in stacks:
                print("=" * 60)
                print(f"Stack Name       : {stack.get('StackName', '<unknown>')}")
                print(f"Stack ID         : {stack.get('StackId', '<unknown>')}")
                print(f"Status           : {stack.get('StackStatus', '<unknown>')}")
                print(f"Creation Time    : {format_dt(stack.get('CreationTime'))}")
                print(f"Last Updated     : {format_dt(stack.get('LastUpdatedTime'))}")
                print(f"Description      : {stack.get('Description', 'No description')}")
                print(f"Tags             : {stack.get('Tags', [])}")
                print(f"Parameters       : {stack.get('Parameters', [])}")
                print(f"Outputs          : {stack.get('Outputs', [])}")
                print(f"Drift Information: {stack.get('DriftInformation', {})}")
                print("=" * 60 + "\n")
    except botocore.exceptions.ClientError as e:
        logger.error("AWS ClientError while describing stacks: %s", e)
    except Exception as e:
        logger.exception("Unexpected error while listing stacks: %s", e)


if __name__ == "__main__":
    list_all_stacks()

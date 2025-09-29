import json
import urllib.parse
import requests
import boto3
import sys
from datetime import datetime, timezone


SESSION_NAME = "test"
DURATION_SECONDS = 43200  # up to 43200 (12h) if your IAM permissions allow


ADMIN_POLICY = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "*",
            "Resource": "*"
        }
    ]
}

def get_federation_console_url(session_name: str, policy: dict, duration: int) -> tuple[str, str]:
    sts = boto3.client("sts")
    resp = sts.get_federation_token(
        Name=session_name,
        Policy=json.dumps(policy),
        DurationSeconds=duration
    )
    creds = resp["Credentials"]
    session_json = {
        "sessionId": creds["AccessKeyId"],
        "sessionKey": creds["SecretAccessKey"],
        "sessionToken": creds["SessionToken"],
    }

    federation_endpoint = "https://signin.aws.amazon.com/federation"
    get_token_url = (
        f"{federation_endpoint}"
        f"?Action=getSigninToken"
        f"&Session={urllib.parse.quote_plus(json.dumps(session_json))}"
    )
    token_response = requests.get(get_token_url)
    if token_response.status_code != 200:
        raise RuntimeError(f"Failed to get signin token: {token_response.text}")
    signin_token = token_response.json()["SigninToken"]

    destination = "https://console.aws.amazon.com/"
    login_url = (
        f"{federation_endpoint}"
        f"?Action=login"
        f"&Issuer=owner"
        f"&Destination={urllib.parse.quote_plus(destination)}"
        f"&SigninToken={urllib.parse.quote_plus(signin_token)}"
    )
    return login_url, creds["Expiration"]

def main():
    try:
        url, expiry = get_federation_console_url(SESSION_NAME, ADMIN_POLICY, DURATION_SECONDS)
    except Exception as e:
        print("Error:", e, file=sys.stderr)
        sys.exit(1)

    print("====== Temporary AWS Console Admin URL ======")
    print(url)
    print()
    print(f"Expires at (UTC): {expiry} (ISO8601)")
    print(f"Generated at (UTC): {datetime.now(timezone.utc).isoformat()}")
    print("WARNING: This URL grants full administrator privileges for the duration. Use it only in trusted, short-lived contexts.")

if __name__ == "__main__":
    main()

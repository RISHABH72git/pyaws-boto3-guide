import boto3

client = boto3.client('cloudfront')


def list_all_distributions():
    distributions = []
    marker = None

    while True:
        if marker:
            response = client.list_distributions(Marker=marker)
        else:
            response = client.list_distributions()

        items = response.get("DistributionList", {}).get("Items", [])
        distributions.extend(items)

        if response["DistributionList"].get("IsTruncated"):
            marker = response["DistributionList"]["NextMarker"]
        else:
            break

    return distributions


distributions = list_all_distributions()
print(f"Found {len(distributions)} CloudFront distributions\n")
for dist in distributions:
    print(f"ID: {dist['Id']}")
    print(f"  ➤ Domain: {dist['DomainName']}")
    print(f"  ➤ Status: {dist['Status']}")
    print(f"  ➤ Enabled: {dist['Enabled']}")
    print(f"  ➤ Comment: {dist.get('Comment', '')}")
    print(f"  ➤ Origins:")
    for origin in dist["Origins"]["Items"]:
        print(f"     - ID: {origin['Id']}, Domain: {origin['DomainName']}")
    print(f"  ➤ Default Root Object: {dist.get('DefaultRootObject', '')}")
    print(f"  ➤ Price Class: {dist.get('PriceClass', '')}")
    print(f"  ➤ Viewer Certificate: {dist.get('ViewerCertificate', {}).get('Certificate', 'N/A')}")
    print("-" * 60)

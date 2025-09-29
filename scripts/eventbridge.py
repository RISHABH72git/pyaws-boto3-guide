import boto3


def list_eventbridge_rules_and_targets(region='us-east-1'):
    client = boto3.client('events', region_name=region)
    buses = client.list_event_buses().get('EventBuses', [])
    result = {}

    for bus in buses:
        bus_name = bus['Name']
        result[bus_name] = {"Rules": []}

        # 2. Paginate through all rules on this bus
        next_token = None
        while True:
            if next_token:
                rule_resp = client.list_rules(EventBusName=bus_name, NextToken=next_token)
            else:
                rule_resp = client.list_rules(EventBusName=bus_name)

            for rule in rule_resp.get('Rules', []):
                rule_entry = {
                    "Name": rule['Name'],
                    "State": rule.get('State'),
                    "EventPattern": rule.get('EventPattern'),
                    "ScheduleExpression": rule.get('ScheduleExpression'),
                    "Description": rule.get('Description'),
                    "Targets": []
                }

                # 3. Get targets for the rule
                targets_resp = client.list_targets_by_rule(Rule=rule['Name'], EventBusName=bus_name)
                for tgt in targets_resp.get('Targets', []):
                    rule_entry["Targets"].append({
                        "Id": tgt.get('Id'),
                        "Arn": tgt.get('Arn'),
                        "Input": tgt.get('Input'),
                        "InputPath": tgt.get('InputPath'),
                        "InputTransformer": tgt.get('InputTransformer')
                    })

                result[bus_name]["Rules"].append(rule_entry)

            next_token = rule_resp.get('NextToken')
            if not next_token:
                break

    return result


def disable_rule(rule_name: str, event_bus_name: str = 'default', region: str = 'us-east-1'):
    """
    Disable a single EventBridge rule.
    """
    client = boto3.client('events', region_name=region)
    client.disable_rule(Name=rule_name, EventBusName=event_bus_name)
    return {"Rule": rule_name, "EventBus": event_bus_name, "Disabled": True}


if __name__ == "__main__":
    details = list_eventbridge_rules_and_targets()
    for bus, info in details.items():
        print(f"\nEvent Bus: {bus}")
        for rule in info["Rules"]:
            print(f"  Rule: {rule['Name']} (State: {rule['State']})")
            for tgt in rule["Targets"]:
                print(f"    - Target: {tgt['Arn']} (Id: {tgt['Id']})")
            print("=" * 100)

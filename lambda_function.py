import json


def lambda_handler(event, context):
    http_method = event.get("httpMethod") or event.get("requestContext", {}).get(
        "http", {}
    ).get("method")

    if http_method and http_method != "POST":
        return {
            "statusCode": 405,
            "body": json.dumps({"error": "Method not allowed"}),
        }

    body = event.get("body", "{}")
    if isinstance(body, str):
        body = json.loads(body or "{}")

    string1 = body.get("string1", "")
    string2 = body.get("string2", "")

    return {
        "statusCode": 200,
        "body": json.dumps({"resultado concatenado ": string1 + string2}),
    }

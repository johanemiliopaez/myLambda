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

    body = event.get("body")

    if body is None:
        body = event
    elif isinstance(body, str):
        body = json.loads(body or "{}")

    string1 = body.get("string1")
    string2 = body.get("string2")

    if string1 is None or string2 is None:
        return {
            "statusCode": 400,
            "body": json.dumps(
                {"error": "Los campos string1 y string2 son obligatorios"}
            ),
        }

    if not isinstance(string1, str) or not isinstance(string2, str):
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Los campos string1 y string2 deben ser texto"}),
        }

    return {
        "statusCode": 200,
        "body": json.dumps({"resultado concatenado ": string1 + string2}),
    }

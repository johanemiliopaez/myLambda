import json


variable_global = "202778"




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

    nombre = body.get("nombre")
    apellido = body.get("apellido")
    edad = body.get("edad")
    correo = body.get("correo")

    if None in (nombre, apellido, edad, correo):
        return {
            "statusCode": 400,
            "body": json.dumps(
                {
                    "error": (
                        "Los campos nombre, apellido, edad y correo son obligatorios, debes incluirlos en el body de la petición"
                    )
                }
            ),
        }

    if not isinstance(nombre, str) or not isinstance(apellido, str):
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Los campos nombre y apellido deben ser texto"}),
        }

    if not isinstance(correo, str):
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "El campo correo debe ser texto"}),
        }

    if not isinstance(edad, int):
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "El campo edad debe ser numerico entero"}),
        }

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "persona": {
                    "nombre": nombre,
                    "apellido": apellido,
                    "edad": edad,
                    "correo": correo,
                }
            }
        ),
    }

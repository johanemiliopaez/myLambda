import os, sys, json, urllib.request

diff = open("/tmp/pr.diff").read()
if len(diff) > 15000:
    diff = diff[:15000] + "\n\n[diff truncado]"

prompt = f"""Eres un experto en seguridad de código Python y AWS Lambda.
Analiza este diff de Pull Request.

Para cada hallazgo usa este formato exacto:
[SEVERIDAD] archivo:línea — descripción
- Detalle técnico
- Recomendación

Severidades: CRITICAL | HIGH | MEDIUM | LOW | INFO

CRITICAL = credenciales hardcodeadas, permisos IAM excesivos, RCE
HIGH = datos sensibles expuestos, variables de entorno inseguras
MEDIUM = manejo de errores peligroso, logging excesivo

Si no hay hallazgos escribe exactamente: "✓ Sin hallazgos relevantes."

DIFF:
````diff
{diff}
```"""

payload = json.dumps({
    "model": "claude-sonnet-4-6",
    "max_tokens": 2048,
    "messages": [{"role": "user", "content": prompt}]
}).encode()

req = urllib.request.Request(
    "https://api.anthropic.com/v1/messages",
    data=payload,
    headers={
        "Content-Type": "application/json",
        "x-api-key": os.environ["ANTHROPIC_API_KEY"],
        "anthropic-version": "2023-06-01"
    }
)

resp = json.loads(urllib.request.urlopen(req).read())
review = resp["content"][0]["text"]
print(review)

has_critical = "[CRITICAL]" in review
with open(os.environ["GITHUB_OUTPUT"], "a") as f:
    f.write(f"has_critical={str(has_critical).lower()}\n")
    f.write(f"review<<EOF\n{review}\nEOF\n")

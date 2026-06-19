import os, json, urllib.request, pathlib

diff = open("/tmp/pr.diff").read()
if len(diff) > 15000:
    diff = diff[:15000] + "\n\n[diff truncado]"

# Lee el prompt desde el archivo separado
prompt_template = pathlib.Path(".github/scripts/prompts/security_review.md").read_text()
prompt = f"{prompt_template}\n\nDIFF:\n```diff\n{diff}\n```"

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
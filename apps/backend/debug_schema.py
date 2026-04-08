import sys

sys.path.insert(0, ".")
from main import app

schema = app.openapi()
print("Security schemes:", schema.get("components", {}).get("securitySchemes", {}))
for path, methods in schema.get("paths", {}).items():
    for method, op in methods.items():
        if isinstance(op, dict) and "security" in op:
            print(f"{method.upper()} {path} security: {op['security']}")

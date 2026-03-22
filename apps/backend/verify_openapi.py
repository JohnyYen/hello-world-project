import sys

sys.path.insert(0, ".")
try:
    from main import app

    print("FastAPI app imported successfully")
except Exception as e:
    print(f"Import error: {e}")
    sys.exit(1)

# Check openapi schema
schema = app.openapi()
print("OpenAPI schema generated")
if "components" in schema and "securitySchemes" in schema["components"]:
    schemes = schema["components"]["securitySchemes"]
    print(f"Security schemes: {list(schemes.keys())}")
    for name, scheme in schemes.items():
        print(
            f"  {name}: type={scheme.get('type')}, scheme={scheme.get('scheme')}, bearerFormat={scheme.get('bearerFormat')}"
        )
else:
    print("No security schemes found")

# Check paths for security requirements
for path, methods in schema.get("paths", {}).items():
    for method, op in methods.items():
        if isinstance(op, dict) and "security" in op:
            print(f"{method.upper()} {path} has security: {op['security']}")

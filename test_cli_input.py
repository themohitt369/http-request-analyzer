
from modules.cli_handler import parse_json_object, validate_headers

print("Test 1: Valid headers and body")

headers = parse_json_object(
    '{"Accept": "application/json"}',
    "Headers"
)

body = parse_json_object(
    '{"name": "Mohit"}',
    "Body"
)

print("Headers:", validate_headers(headers))
print("Body:", body)

print("\nTest 2: Invalid JSON")

try:
    parse_json_object("{bad json}", "Body")
except ValueError as exc:
    print("Expected validation error:", exc)
else:
    print("FAIL: Invalid JSON was accepted")

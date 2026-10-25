
from modules.security_utils import SecurityUtils


security = SecurityUtils()

# Test 1: Sensitive HTTP headers
headers = {
    "Accept": "application/json",
    "Authorization": "Bearer example-secret",
    "X-API-Key": "sample-api-key",
    "Cookie": "sessionid=example-session",
}

safe_headers = security.redact_headers(headers)

assert safe_headers["Accept"] == "application/json"
assert safe_headers["Authorization"] == "[REDACTED]"
assert safe_headers["X-API-Key"] == "[REDACTED]"
assert safe_headers["Cookie"] == "[REDACTED]"
assert headers["Authorization"] == "Bearer example-secret"

print("Test 1 passed: Headers redacted; original preserved")

# Test 2: Nested dictionaries
data = {
    "user": {
        "username": "test-user",
        "password": "example-password",
    },
    "access_token": "example-token",
    "items": [
        {"name": "Laptop", "client_secret": "example-secret"},
        {"name": "Mouse"},
    ],
}

safe_data = security.redact_data(data)

assert safe_data["user"]["password"] == "[REDACTED]"
assert safe_data["access_token"] == "[REDACTED]"
assert safe_data["items"][0]["client_secret"] == "[REDACTED]"
assert safe_data["items"][0]["name"] == "Laptop"
assert data["user"]["password"] == "example-password"

print("Test 2 passed: Nested data redacted; original preserved")

# Test 3: Plain text redaction
text = (
    "Authorization: Bearer abc123 "
    "api_key=secret123 password='my password'"
)

safe_text = security.redact_text(text)

assert "abc123" not in safe_text
assert "secret123" not in safe_text
assert "my password" not in safe_text
assert "[REDACTED]" in safe_text

print("Test 3 passed: Common text secrets redacted")

# Test 4: Type validation
for function, value in [
    (security.redact_headers, ["not", "a", "dict"]),
    (security.redact_text, {"not": "text"}),
]:
    try:
        function(value)
    except TypeError:
        pass
    else:
        raise AssertionError("Expected TypeError for invalid input")

print("Test 4 passed: Invalid input types rejected")

print("\nAll security utility tests passed.")

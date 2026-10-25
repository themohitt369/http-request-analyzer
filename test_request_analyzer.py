
from modules.request_analyzer import RequestAnalyzer


analyzer = RequestAnalyzer()

request_data = {
    "url": "https://httpbin.org/post?token=example-secret#section",
    "method": "POST",
    "headers": {
        "Accept": "application/json",
        "Authorization": "Bearer example-secret",
        "Content-Type": "application/json",
    },
    "body": {
        "product": "Laptop",
        "quantity": 2,
    },
    "timeout": 10.0,
}

result = analyzer.analyze_request(request_data)

print("Request Analysis:")
for key, value in result.items():
    print(f"{key}: {value}")

assert result["method"] == "POST"
assert result["scheme"] == "https"
assert result["hostname"] == "httpbin.org"
assert result["path"] == "/post"
assert result["header_count"] == 3
assert result["headers"]["Authorization"] == "[REDACTED]"
assert "token=" not in result["url"]
assert result["body_present"] is True
assert result["body_field_count"] == 2

print("\nAll request analyzer tests passed.")

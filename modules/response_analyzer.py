import json


class ResponseAnalyzer:
    """Extract useful metadata from an HTTP response."""

    SENSITIVE_HEADERS = {
        "authorization",
        "proxy-authorization",
        "cookie",
        "set-cookie",
        "x-api-key",
    }

    def analyze_response(self, response):
        """Analyze a requests.Response object."""

        headers = dict(response.headers)

        # Redact sensitive response-header values.
        safe_headers = {}
        for name, value in headers.items():
            if name.lower() in self.SENSITIVE_HEADERS:
                safe_headers[name] = "[REDACTED]"
            else:
                safe_headers[name] = value

        content_type = response.headers.get("Content-Type", "")
        response_body = response.content

        # Check whether the body is valid JSON without returning the body itself,which contain sensitive information.
        is_json = "json" in content_type.lower()
        json_valid = None

        if is_json:
            try:
                json.loads(response_body)
                json_valid = True
            except (json.JSONDecodeError, UnicodeDecodeError):
                json_valid = False

        return {
            "status_code": response.status_code,
            "reason": response.reason,
            "url": response.url,
            "content_type": content_type,
            "content_length_header": response.headers.get("Content-Length"),
            "response_size_bytes": len(response_body),
            "elapsed_seconds": response.elapsed.total_seconds(),
            "header_count": len(response.headers),
            "headers": safe_headers,
            "is_json_content_type": is_json,
            "json_valid": json_valid,
            "redirect_count": len(response.history),
            "is_success_status": 200 <= response.status_code < 300,
        }

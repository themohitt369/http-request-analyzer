from urllib.parse import urlparse


class RequestAnalyzer:
    """Analyze and summarize HTTP request data."""

    SENSITIVE_HEADERS = {
        "authorization",
        "proxy-authorization",
        "cookie",
        "set-cookie",
        "x-api-key",
    }

    def analyze_request(self, request_data):
        """Return a structure summary of a request."""

        url = request_data.get("url", "")
        method = request_data.get("method", "GET").upper()
        headers = request_data.get("headers", {})
        body = request_data.get("body", {})
        timeout = request_data.get("timeout", 10.0)

        parsed_url = urlparse(url)

        # Avoid exposing credentials embedded in a URL.
        safe_netloc = parsed_url.hostname or ""
        if parsed_url.port:
            safe_netloc += f":{parsed_url.port}"

        safe_url = parsed_url._replace(
            netloc=safe_netloc,
            query="",
            fragment="",
        ).geturl()

        # Keep header names,but redact sensitive values.
        safe_headers = {}
        for name, values in headers.items():
            if name.lower() in self.SENSITIVE_HEADERS:
                safe_headers[name] = "[REDACTED]"
            else:
                safe_headers[name] = values

        body_present = bool(body)

        return {
            "method": method,
            "url": safe_url,
            "scheme": parsed_url.scheme,
            "hostname": parsed_url.hostname,
            "path": parsed_url.path or "/",
            "headers": safe_headers,
            "header_count": len(headers),
            "body_present": body_present,
            "body_type": type(body).__name__,
            "body_field_count": len(body) if isinstance(body, dict) else None,
            "timeout_seconds": timeout,
        }

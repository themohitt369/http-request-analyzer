
import re


class SecurityUtils:
    """Redact sensitive values before displaying or reporting data."""

    SENSITIVE_KEYS = {
        "authorization",
        "proxy-authorization",
        "cookie",
        "set-cookie",
        "x-api-key",
        "api-key",
        "apikey",
        "password",
        "passwd",
        "secret",
        "client_secret",
        "access_token",
        "refresh_token",
        "token",
        "session",
        "sessionid",
        "credentials",
        "private_key",
    }

    REDACTED = "[REDACTED]"

    def is_sensitive_key(self, key):
        """Check whether a field name indicates sensitive data."""

        normalized = re.sub(r"[^a-z0-9]", "", str(key).lower())

        sensitive_normalized = {
            re.sub(r"[^a-z0-9]", "", name)
            for name in self.SENSITIVE_KEYS
        }

        if normalized in sensitive_normalized:
            return True

        # Catch common compound names, e.g. user_password or auth_token.
        sensitive_terms = (
            "password",
            "passwd",
            "secret",
            "token",
            "apikey",
            "authorization",
            "credential",
            "privatekey",
            "sessionid",
        )

        return any(term in normalized for term in sensitive_terms)

    def redact_data(self, data):
        """Recursively redact sensitive dictionary fields."""

        if isinstance(data, dict):
            cleaned = {}

            for key, value in data.items():
                if self.is_sensitive_key(key):
                    cleaned[key] = self.REDACTED
                else:
                    cleaned[key] = self.redact_data(value)

            return cleaned

        if isinstance(data, list):
            return [self.redact_data(item) for item in data]

        if isinstance(data, tuple):
            return tuple(self.redact_data(item) for item in data)

        return data

    def redact_headers(self, headers):
        """Return a sanitized copy of an HTTP headers dictionary."""

        if not isinstance(headers, dict):
            raise TypeError("Headers must be a dictionary.")

        return self.redact_data(headers)

    def redact_text(self, text):
        """Redact common secret assignments in plain text."""

        if not isinstance(text, str):
            raise TypeError("Text input must be a string.")

        patterns = [
            (
                r'(?i)\b(authorization\s*[:=]\s*)(?:bearer\s+)?'
                r'[^,\s;]+',
                r'\1[REDACTED]',
            ),
            (
                r'(?i)\b((?:access[_-]?token|refresh[_-]?token|'
                r'api[_-]?key|client[_-]?secret|password|passwd|'
                r'token|secret)\s*[:=]\s*)'
                r'(?:"[^"]*"|\'[^\']*\'|[^,\s;&]+)',
                r'\1[REDACTED]',
            ),
        ]

        cleaned = text
        for pattern, replacement in patterns:
            cleaned = re.sub(pattern, replacement, cleaned)

        return cleaned

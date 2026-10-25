
import json
from urllib.parse import urlsplit

ALLOWED_METHODS = {"GET", "POST", "PUT", "DELETE"}
DEFAULT_TIMEOUT = 10.0
MAX_TIMEOUT = 60.0


def validate_url(url):
    """Validate basic HTTP/HTTPS URL structure."""
    if not isinstance(url, str) or not url.strip():
        raise ValueError("URL cannot be empty.")

    url = url.strip()

    try:
        parsed = urlsplit(url)

        if parsed.scheme.lower() not in {"http", "https"}:
            raise ValueError("Only HTTP and HTTPS URLs are allowed.")

        if not parsed.hostname:
            raise ValueError("URL must contain a valid hostname.")

        # Accessing .port also validates malformed port syntax.
        if parsed.port is not None and not (1 <= parsed.port <= 65535):
            raise ValueError("Port must be between 1 and 65535.")

        if parsed.username is not None or parsed.password is not None:
            raise ValueError("Do not put credentials inside the URL.")

    except ValueError as exc:
        raise ValueError(f"Invalid URL: {exc}") from exc

    return url


def validate_method(method):
    """Accept only supported HTTP methods."""
    method = method.strip().upper()

    if method not in ALLOWED_METHODS:
        raise ValueError("Method must be GET, POST, PUT, or DELETE.")

    return method


def parse_json_object(raw_text, field_name):
    """Parse optional JSON input and require a JSON object."""
    if not raw_text.strip():
        return {}

    try:
        value = json.loads(raw_text)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"{field_name} must contain valid JSON: {exc.msg}"
        ) from exc

    if not isinstance(value, dict):
        raise ValueError(
            f"{field_name} must be a JSON object, for example {{}}."
        )

    return value


def validate_headers(headers):
    """Validate basic HTTP header names and values."""
    validated = {}
    separators = set('()<>@,;:\\"/[]?={} \t')

    for name, value in headers.items():
        if not isinstance(name, str) or not name:
            raise ValueError("Header names cannot be empty.")

        if any(
            ord(char) < 33 or ord(char) > 126 or char in separators
            for char in name
        ):
            raise ValueError(f"Invalid HTTP header name: {name!r}")

        if not isinstance(value, str):
            raise ValueError(
                f"Header value for {name!r} must be a string."
            )

        if "\r" in value or "\n" in value:
            raise ValueError(
                f"Header value for {name!r} cannot contain newlines."
            )

        validated[name] = value

    return validated


def validate_timeout(raw_timeout):
    """Require a positive timeout no greater than 60 seconds."""
    try:
        timeout = float(raw_timeout)
    except (TypeError, ValueError) as exc:
        raise ValueError("Timeout must be a number.") from exc

    if not 0 < timeout <= MAX_TIMEOUT:
        raise ValueError(
            "Timeout must be greater than 0 and at most 60."
        )

    return timeout


def prompt_until_valid(prompt, validator):
    """Repeat a prompt until its value passes validation."""
    while True:
        raw_value = input(prompt)

        try:
            return validator(raw_value)
        except ValueError as exc:
            print(f"Input error: {exc}")


def collect_request_input():
    """Collect and validate inputs without sending an HTTP request."""
    print("\n--- HTTP Request Analyzer ---")

    url = prompt_until_valid(
        "Enter URL (http:// or https://): ",
        validate_url,
    )

    method = prompt_until_valid(
        "HTTP method (GET/POST/PUT/DELETE): ",
        validate_method,
    )

    print(
        '\nOptional headers: enter a JSON object, '
        'e.g. {"Accept":"application/json"}'
    )
    headers = prompt_until_valid(
        "Headers (press Enter to skip): ",
        lambda raw: validate_headers(
            parse_json_object(raw, "Headers")
        ),
    )

    print(
        '\nOptional JSON body: enter a JSON object, '
        'e.g. {"name":"Mohit Pal"}'
    )
    body = prompt_until_valid(
        "Body (press Enter to skip): ",
        lambda raw: parse_json_object(raw, "Body"),
    )

    timeout = prompt_until_valid(
        f"Timeout in seconds (default {DEFAULT_TIMEOUT}): ",
        lambda raw: validate_timeout(
            raw if raw.strip() else DEFAULT_TIMEOUT
        ),
    )

    return {
        "url": url,
        "method": method,
        "headers": headers,
        "body": body,
        "timeout": timeout,
    }


import requests


class RequestSender:
    """Send HTTP requests and capture transport errors."""

    def __init__(self):
        self.session = requests.Session()

    def send_request(self, request_data):
        """Send a validated request and return its result."""
        url = request_data["url"]
        method = request_data["method"].upper()
        headers = request_data.get("headers", {})
        body = request_data.get("body", {})
        timeout = request_data.get("timeout", 10.0)

        allowed_methods = {"GET", "POST", "PUT", "DELETE"}

        if method not in allowed_methods:
            return {
                "success": False,
                "error_type": "ValidationError",
                "error": "Unsupported HTTP method.",
            }

        try:
            response = self.session.request(
                method=method,
                url=url,
                headers=headers,
                json=body if body else None,
                timeout=timeout,
                allow_redirects=False,
            )

            return {
                "success": True,
                "response": response,
                "error_type": None,
                "error": None,
            }

        except requests.exceptions.Timeout:
            return {
                "success": False,
                "error_type": "Timeout",
                "error": "The HTTP request timed out.",
            }

        except requests.exceptions.SSLError:
            return {
                "success": False,
                "error_type": "SSLError",
                "error": "TLS/SSL verification failed.",
            }

        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "error_type": "ConnectionError",
                "error": "Could not connect to the destination.",
            }

        except requests.exceptions.RequestException:
            return {
                "success": False,
                "error_type": "RequestError",
                "error": "The HTTP request could not be completed.",
            }

    def close(self):
        """Close the session and release its resources."""
        self.session.close()

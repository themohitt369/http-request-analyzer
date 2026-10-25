
import json


class JSONParser:
    """Parse and validate JSON text or HTTP responses."""

    def parse_text(self, raw_text):
        """Parse JSON text and return a structured result."""

        if not isinstance(raw_text, str):
            return {
                "success": False,
                "error_type": "InputTypeError",
                "error": "JSON input must be a string.",
                "data": None,
                "data_type": None,
                "item_count": None,
            }

        if not raw_text.strip():
            return {
                "success": False,
                "error_type": "EmptyInput",
                "error": "JSON input is empty.",
                "data": None,
                "data_type": None,
                "item_count": None,
            }

        try:
            data = json.loads(raw_text)

            if isinstance(data, dict):
                data_type = "object"
                item_count = len(data)
            elif isinstance(data, list):
                data_type = "array"
                item_count = len(data)
            elif data is None:
                data_type = "null"
                item_count = None
            else:
                data_type = type(data).__name__
                item_count = None

            return {
                "success": True,
                "error_type": None,
                "error": None,
                "data": data,
                "data_type": data_type,
                "item_count": item_count,
            }

        except json.JSONDecodeError as exc:
            return {
                "success": False,
                "error_type": "JSONDecodeError",
                "error": (
                    f"Invalid JSON at line {exc.lineno}, "
                    f"column {exc.colno}."
                ),
                "data": None,
                "data_type": None,
                "item_count": None,
            }

    def parse_response(self, response):
        """Parse an HTTP response only when its content type is JSON."""

        content_type = response.headers.get("Content-Type", "").lower()

        is_json = (
            "application/json" in content_type
            or content_type.endswith("+json")
            or "+json;" in content_type
        )

        if not is_json:
            return {
                "success": False,
                "error_type": "NonJSONResponse",
                "error": "Response Content-Type does not indicate JSON.",
                "data": None,
                "data_type": None,
                "item_count": None,
            }

        try:
            # Requests decodes the response bytes according to its
            # response encoding before returning response.text.
            raw_text = response.text
        except Exception:
            return {
                "success": False,
                "error_type": "ResponseReadError",
                "error": "Could not read the response body.",
                "data": None,
                "data_type": None,
                "item_count": None,
            }

        return self.parse_text(raw_text)

class StatusCodeInterpreter:
    """ Interpreter HTTP status codes and provide troubleshooting guidance. """

    STATUS_INFO={
        200:(
            "OK",
            "The request was successful.",
            "No action required."
        ),
        201:(
            "Created",
            "The request succeeded and created a resource.",
            "Verify the created resource if needed."
        ),
        202:(
            "Accepted",
            "The request was accepted for processing.",
            "Check the processing result if the operation is asynchronous."
        ),
        204: (
            "No Content",
            "The request succeeded without a response body.",
            "An empty body is expected for this status."
        ),
        301: (
            "Moved Permanently",
            "The resource has a permanent redirect.",
            "Check the Location header and confirm the destination."
        ),
        302: (
            "Found",
            "The resource is temporarily redirected.",
            "Check the Location header and redirect behavior."
        ),
        304: (
            "Not Modified",
            "The cached resource has not changed.",
            "Use the cached version when applicable."
        ),
        400: (
            "Bad Request",
            "The server rejected the request as invalid.",
            "Check request syntax, parameters, headers, and body."
        ),
        401: (
            "Unauthorized",
            "Authentication is missing or invalid.",
            "Check authentication configuration without exposing credentials."
        ),
        403: (
            "Forbidden",
            "The server refused to authorize the request.",
            "Check permissions and access policy."
        ),
        404: (
            "Not Found",
            "The requested resource was not found.",
            "Check the URL, path, and resource availability."
        ),
        405: (
            "Method Not Allowed",
            "The endpoint does not allow this HTTP method.",
            "Check the endpoint's supported methods."
        ),
        408: (
            "Request Timeout",
            "The server timed out waiting for the request.",
            "Check network conditions and server behavior."
        ),
        409: (
            "Conflict",
            "The request conflicts with the current resource state.",
            "Check resource state and API conflict requirements."
        ),
        415: (
            "Unsupported Media Type",
            "The server does not support the request body format.",
            "Check the Content-Type header and supported formats."
        ),
        422: (
            "Unprocessable Content",
            "The request format may be valid, but its instructions cannot be processed.",
            "Check field values and validation requirements."
        ),
        429: (
            "Too Many Requests",
            "The client sent too many requests in a given period.",
            "Respect rate limits and any Retry-After header."
        ),
        500: (
            "Internal Server Error",
            "The server encountered an unexpected condition.",
            "Check server logs or contact the API owner."
        ),
        502: (
            "Bad Gateway",
            "A gateway received an invalid upstream response.",
            "Check upstream service and gateway health."
        ),
        503: (
            "Service Unavailable",
            "The server is temporarily unable to handle the request.",
            "Check service status and any Retry-After header."
        ),
        504: (
            "Gateway Timeout",
            "A gateway did not receive a timely upstream response.",
            "Check upstream latency and gateway timeout configuration."
        ),
    }

    def interpret(self, status_code):
        """Return interpretation for an HTTP status code."""

        if isinstance(status_code, bool) or not isinstance(status_code, int):
            raise ValueError("Status code must be an integer.")

        if not 100 <= status_code <= 599:
            raise ValueError("Status code must be between 100 and 599.")

        if status_code in self.STATUS_INFO:
            phrase, meaning, guidance = self.STATUS_INFO[status_code]
        else:
            phrase = "Unknown or unlisted status"
            meaning = (
                "This status code is not included in the tool's built-in "
                "reference dictionary."
            )
            guidance = (
                "Consult the API documentation or the HTTP status-code registry."
            )

        if 100 <= status_code <= 199:
            category = "Informational"
        elif 200 <= status_code <= 299:
            category = "Success"
        elif 300 <= status_code <= 399:
            category = "Redirection"
        elif 400 <= status_code <= 499:
            category = "Client Error"
        else:
            category = "Server Error"

        return {
            "status_code": status_code,
            "phrase": phrase,
            "category": category,
            "meaning": meaning,
            "guidance": guidance,
        }

    
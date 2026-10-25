
from modules.request_sender import RequestSender


def run_test(sender, test_name, request_data):
    print(f"\n{'=' * 50}")
    print(f"TEST: {test_name}")
    print("=" * 50)

    result = sender.send_request(request_data)

    print("Success:", result["success"])

    if result["success"]:
        response = result["response"]
        print("Status Code:", response.status_code)
        print("Content-Type:", response.headers.get("Content-Type"))
        print("Redirect Followed:", bool(response.history))

        # HTTP 4xx/5xx responses are still valid HTTP responses.
        if response.status_code >= 400:
            print("HTTP Error Status: Yes")
        else:
            print("HTTP Error Status: No")

    else:
        print("Error Type:", result["error_type"])
        print("Error Message:", result["error"])


def main():
    sender = RequestSender()

    common_headers = {
        "Accept": "application/json"
    }

    tests = [
        (
            "GET Request",
            {
                "url": "https://httpbin.org/get",
                "method": "GET",
                "headers": common_headers,
                "body": {},
                "timeout": 10.0,
            },
        ),
        (
            "POST Request",
            {
                "url": "https://httpbin.org/post",
                "method": "POST",
                "headers": common_headers,
                "body": {"name": "Test User", "project": "HTTP Analyzer"},
                "timeout": 10.0,
            },
        ),
        (
            "PUT Request",
            {
                "url": "https://httpbin.org/put",
                "method": "PUT",
                "headers": common_headers,
                "body": {"name": "Updated User"},
                "timeout": 10.0,
            },
        ),
        (
            "DELETE Request",
            {
                "url": "https://httpbin.org/delete",
                "method": "DELETE",
                "headers": common_headers,
                "body": {},
                "timeout": 10.0,
            },
        ),
        (
            "Invalid Method",
            {
                "url": "https://httpbin.org/get",
                "method": "PATCH",
                "headers": common_headers,
                "body": {},
                "timeout": 10.0,
            },
        ),
        (
            "Timeout Test",
            {
                "url": "https://httpbin.org/delay/3",
                "method": "GET",
                "headers": common_headers,
                "body": {},
                "timeout": 0.001,
            },
        ),
        (
            "Connection Error Test",
            {
                "url": "http://127.0.0.1:1/",
                "method": "GET",
                "headers": common_headers,
                "body": {},
                "timeout": 2.0,
            },
        ),
    ]

    try:
        for test_name, request_data in tests:
            try:
                run_test(sender, test_name, request_data)
            except Exception as error:
                # Keep later tests running if a test script itself fails.
                print("TEST SCRIPT ERROR:", type(error).__name__, str(error))

    finally:
        sender.close()
        print("\nAll test cases have finished.")

    
if __name__ == "__main__":
    main()

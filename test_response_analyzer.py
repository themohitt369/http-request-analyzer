
from modules.request_sender import RequestSender
from modules.response_analyzer import ResponseAnalyzer


sender = RequestSender()
analyzer = ResponseAnalyzer()

request_data = {
    "url": "https://httpbin.org/get",
    "method": "GET",
    "headers": {"Accept": "application/json"},
    "body": {},
    "timeout": 10.0,
}

try:
    result = sender.send_request(request_data)

    if not result["success"]:
        print("Request failed:")
        print("Error type:", result["error_type"])
        print("Error:", result["error"])
    else:
        response = result["response"]
        analysis = analyzer.analyze_response(response)

        print("Response Analysis:")
        for key, value in analysis.items():
            print(f"{key}: {value}")

        assert analysis["status_code"] == 200
        assert analysis["is_success_status"] is True
        assert analysis["is_json_content_type"] is True
        assert analysis["json_valid"] is True
        assert analysis["response_size_bytes"] >= 0

        print("\nAll response analyzer tests passed.")

finally:
    sender.close()

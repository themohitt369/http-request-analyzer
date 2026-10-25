
from modules.cli_handler import collect_request_input
from modules.request_sender import RequestSender
from modules.request_analyzer import RequestAnalyzer
from modules.response_analyzer import ResponseAnalyzer
from modules.status_interpreter import StatusCodeInterpreter
from modules.json_parser import JSONParser
from modules.report_generator import JSONReportGenerator


def safe_json_parse_summary(parse_result):
    """Keep JSON parsing metadata, but exclude the parsed response data."""
    return {
        "success": parse_result.get("success", False),
        "error_type": parse_result.get("error_type"),
        "error": parse_result.get("error"),
        "data_type": parse_result.get("data_type"),
        "item_count": parse_result.get("item_count"),
    }


def main():
    print("=" * 55)
    print("          HTTP REQUEST ANALYZER")
    print("=" * 55)

    sender = RequestSender()
    report_generator = JSONReportGenerator()

    request_analysis = {}
    response_analysis = {}
    status_interpretation = {}
    json_parse_result = {}
    request_error = None

    try:
        # 1. Collect and validate the user's request.
        request_data = collect_request_input()

        # 2. Analyze the request without exposing sensitive values.
        request_analysis = RequestAnalyzer().analyze_request(
            request_data
        )

        print("\n[+] Request prepared.")
        print(f"    Method: {request_analysis['method']}")
        print(f"    URL: {request_analysis['url']}")

        # 3. Send the HTTP request.
        print("\n[*] Sending HTTP request...")
        send_result = sender.send_request(request_data)

        if not send_result.get("success"):
            request_error = {
                "error_type": send_result.get(
                    "error_type", "RequestError"
                ),
                "message": send_result.get(
                    "error", "The request could not be completed."
                ),
            }
            print("\n[!] Request failed.")
            print(f"    Reason: {request_error['message']}")

        else:
            response = send_result["response"]

            # 4. Analyze response metadata.
            response_analysis = ResponseAnalyzer().analyze_response(
                response
            )

            # Never record a potentially sensitive query string.
            response_analysis["url"] = request_analysis["url"]

            # 5. Interpret the HTTP status code.
            status_interpretation = StatusCodeInterpreter().interpret(
                response.status_code
            )

            print("\n[+] HTTP response received.")
            print(
                f"    Status: {response.status_code} "
                f"{response.reason}"
            )
            print(
                f"    Category: "
                f"{status_interpretation['category']}"
            )
            print(
                f"    Meaning: "
                f"{status_interpretation['meaning']}"
            )
            print(
                f"    Response size: "
                f"{response_analysis['response_size_bytes']} bytes"
            )

            # 6. Parse JSON only when the response declares JSON.
            if response_analysis["is_json_content_type"]:
                parse_result = JSONParser().parse_response(response)

                # Keep metadata only; do not include raw parsed data.
                json_parse_result = safe_json_parse_summary(
                    parse_result
                )

                if parse_result.get("success"):
                    print("\n[+] Response contains valid JSON.")
                    print(
                        f"    JSON type: "
                        f"{parse_result.get('data_type')}"
                    )
                    print(
                        f"    Top-level item count: "
                        f"{parse_result.get('item_count')}"
                    )
                else:
                    print("\n[!] JSON parsing was unsuccessful.")
                    print(
                        f"    Reason: "
                        f"{parse_result.get('error')}"
                    )
            else:
                json_parse_result = {
                    "success": False,
                    "error_type": "NonJSONResponse",
                    "error": (
                        "Response Content-Type does not indicate JSON."
                    ),
                    "data_type": None,
                    "item_count": None,
                }
                print("\n[*] Response is not declared as JSON.")

    except (KeyboardInterrupt, EOFError):
        request_error = {
            "error_type": "UserCancelled",
            "message": "The operation was cancelled by the user.",
        }
        print("\n[!] Operation cancelled.")

    except (ValueError, TypeError) as exc:
        # Validation errors may be shown to the user, but never print
        # request bodies, credentials, or the raw HTTP response.
        request_error = {
            "error_type": "InputError",
            "message": str(exc),
        }
        print(f"\n[!] Input error: {exc}")

    except Exception:
        # Do not expose unexpected exception details, which may contain
        # sensitive request or environment information.
        request_error = {
            "error_type": "UnexpectedError",
            "message": (
                "An unexpected error occurred. "
                "Check the input and try again."
            ),
        }
        print("\n[!] An unexpected error occurred.")

    finally:
        # Release the Requests session even when an error occurs.
        sender.close()

    # 7. Generate a report for success, HTTP errors, or request failures.
    try:
        report_path = report_generator.generate_and_save(
            request_analysis=request_analysis,
            response_analysis=response_analysis,
            status_interpretation=status_interpretation,
            json_parse_result=json_parse_result,
            request_error=request_error,
        )
        print("\n[+] Report saved successfully.")
        print(f"    Report path: {report_path.resolve()}")

    except (OSError, ValueError, TypeError):
        print("\n[!] Could not save the JSON report.")
        print("    Check the reports directory and permissions.")

    print("\n" + "=" * 55)
    print("              ANALYSIS FINISHED")
    print("=" * 55)


if __name__ == "__main__":
    main()

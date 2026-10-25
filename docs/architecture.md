# HTTP Request Analyzer — Architecture

## 1. Overview

HTTP Request Analyzer is a modular Python command-line application for sending HTTP requests, analyzing request and response metadata, interpreting HTTP status codes, parsing JSON data, redacting sensitive information, and generating JSON reports.

The application separates input handling, request execution, response analysis, security utilities, and report generation into individual modules.

## 2. Project Structure

```text
http-request-analyzer/
├── main.py
├── modules/
│   ├── __init__.py
│   ├── cli_handler.py
│   ├── json_parser.py
│   ├── report_generator.py
│   ├── request_analyzer.py
│   ├── request_sender.py
│   ├── response_analyzer.py
│   ├── security_utils.py
│   └── status_interpreter.py
├── tests/
│   └── test_automated_suite.py
├── reports/
├── docs/
│   └── architecture.md
├── requirements.txt
├── .gitignore
├── README.md
└── LICENSE
```

## 3. Module Responsibilities

### main.py

The application's entry point.

- `main()` coordinates the application workflow.
- `safe_json_parse_summary()` prepares a summary of JSON parsing results.

### cli_handler.py

Handles command-line input and validation.

- `validate_url()` validates the supplied URL.
- `validate_method()` validates the HTTP method.
- `parse_json_object()` parses and validates JSON objects.
- `validate_headers()` validates request headers.
- `validate_timeout()` validates the timeout value.
- `prompt_until_valid()` repeats a prompt until valid input is supplied.
- `collect_request_input()` collects request information.

### request_analyzer.py

Defines `RequestAnalyzer`.

- `analyze_request()` analyzes the supplied request data and prepares structured request-analysis information.

### request_sender.py

Defines `RequestSender`.

- `send_request()` sends the HTTP request and handles relevant request errors.
- `close()` closes the associated request session or resources.

### response_analyzer.py

Defines `ResponseAnalyzer`.

- `analyze_response()` analyzes the received HTTP response and prepares response metadata.

### status_interpreter.py

Defines `StatusCodeInterpreter`.

- `interpret()` interprets an HTTP status code.

### json_parser.py

Defines `JSONParser`.

- `parse_text()` parses JSON text and handles parsing outcomes.
- `parse_response()` processes a response when JSON parsing is applicable.

### security_utils.py

Defines `SecurityUtils`.

- `is_sensitive_key()` checks whether a key should be treated as sensitive.
- `redact_data()` redacts sensitive information in supported data structures.
- `redact_headers()` handles sensitive header values.
- `redact_text()` redacts sensitive information in supported text.

Redaction reduces the risk of exposing sensitive information but cannot guarantee that every secret will be detected.

### report_generator.py

Defines `JSONReportGenerator`.

- `generate_report()` prepares a structured report.
- `save_report()` saves the report to a file.
- `generate_and_save()` coordinates report creation and saving.

## 4. High-Level Workflow

1. The application starts through `main.py`.
2. The CLI handler collects and validates request details.
3. The request analyzer processes the supplied request information.
4. The request sender attempts to send the HTTP request.
5. The response analyzer examines the response when one is received.
6. The status interpreter interprets the HTTP status code.
7. The JSON parser processes JSON data when applicable.
8. Security utilities redact sensitive information where integrated into the workflow.
9. The report generator prepares and saves a JSON report.
10. Request resources are closed when required.

The exact execution order and error-handling branches depend on the implementation in `main.py`.

## 5. Automated Testing

The automated test suite is located at `tests/test_automated_suite.py`.

Run the suite from the project root:

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
```

The suite covers input validation, request handling, status interpretation, sensitive-data redaction, JSON processing, and report generation.

## 6. Design Principles

- **Modularity:** Responsibilities are separated across modules.
- **Input validation:** Request details are checked before execution.
- **Error handling:** Common request failures are handled explicitly.
- **Security awareness:** Sensitive values are redacted where supported.
- **Structured output:** JSON provides machine-readable reports.
- **Testability:** Automated tests verify core behaviors.

## 7. Security Scope

This application is intended for educational use and authorized HTTP testing. It is not a full web vulnerability scanner and does not prove that a target application is secure.

Review generated reports before sharing them. Avoid using real credentials, API keys, session cookies, or other secrets in test requests.

# HTTP Request Analyzer

A Python-based command-line tool for sending HTTP requests, analyzing request and response metadata, interpreting HTTP status codes, parsing JSON responses, and generating sanitized JSON reports.

## Features

- Supports GET, POST, PUT, and DELETE HTTP methods.
- Validates URLs, HTTP methods, timeout values, headers, and JSON request bodies.
- Sends HTTP requests using Python's Requests library.
- Analyzes HTTP request and response metadata.
- Interprets HTTP status codes and their meanings.
- Parses JSON responses when applicable.
- Redacts sensitive information from relevant output and reports.
- Generates structured JSON reports for analysis.
- Handles common request errors, including connection failures and timeouts.
- Includes an automated test suite using Python's `unittest` framework.

## Project Architecture

```text
http-request-analyzer/
│
├── main.py
│
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
│
├── tests/
│   └── test_automated_suite.py
│
├── reports/
├── docs/
│
├── requirements.txt
├── .gitignore
├── README.md
└── LICENSE
```

## Technology Stack

- **Python** — Core programming language.
- **Requests** — HTTP request handling.
- **JSON** — Request-body parsing and report serialization.
- **unittest** — Automated testing.
- **Git and GitHub** — Version control and project hosting.

## How It Works

The application follows a modular processing workflow:

1. **Input Collection:** Collects request details through the command-line interface.
2. **Input Validation:** Validates the URL, HTTP method, timeout, headers, and request body.
3. **Request Analysis:** Processes and analyzes the supplied request information.
4. **HTTP Request Execution:** Sends the request using the Requests library.
5. **Response Analysis:** Examines response metadata, including the HTTP status code and headers.
6. **Status Interpretation:** Provides an interpretation of the returned HTTP status.
7. **JSON Processing:** Parses the response when it contains supported JSON data.
8. **Security Handling:** Redacts sensitive information where applicable.
9. **Report Generation:** Generates a JSON report containing relevant analysis results.

## Installation

### Prerequisites

- Python installed on your system.
- Git, if you want to clone the repository.
- An internet connection for requests to external HTTP endpoints.

### 1. Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd http-request-analyzer
```

Replace `<YOUR_GITHUB_REPOSITORY_URL>` with the actual GitHub repository URL after publishing the project.

Alternatively, download the repository and open its root directory in a terminal.

### 2. Create a Virtual Environment

**Windows PowerShell:**

```powershell
python -m venv .vir_env
.\.vir_env\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can run the program using the virtual environment's Python executable directly instead of changing your system's execution policy.

### 3. Install Dependencies

```powershell
python -m pip install -r requirements.txt
```

## Usage

Run the application from the project root directory:

```powershell
python main.py
```

Follow the command-line prompts and provide the request details requested by the application, such as:

- Target URL
- HTTP method
- Request headers
- JSON request body, when applicable
- Request timeout

Use valid inputs and review the results produced by the application. Generated reports are stored in the project's `reports/` directory, according to the report-generation configuration.

## Running Automated Tests

Run the automated test suite from the project root directory:

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
```

The automated suite covers important components, including:

- Input validation
- HTTP request handling
- Request parameter forwarding
- Timeout and connection-error handling
- HTTP status interpretation
- Sensitive-data redaction
- JSON serialization and deserialization
- Report generation and saving
- Report filename and content checks

A successful test run should finish with `OK`. The number of tests may change as the project evolves.

## Reports

The application generates JSON reports in the `reports/` directory.

Reports can be used to review request and response analysis results and to retain structured records of testing sessions.

Before sharing a report publicly, inspect its contents and confirm that it does not contain sensitive data.

## Error Handling

The application includes handling for common request-related failures, such as:

- Invalid input
- Connection errors
- Request timeouts
- HTTP error status codes
- Invalid or unsupported JSON data, where applicable

An HTTP response with a status such as `404` or `500` is not necessarily a transport failure. The request may have reached the server successfully even when the server returns an error status.

## Security and Ethical Use

This project is intended for educational purposes and authorized HTTP testing.

- Test only systems and endpoints that you own or have explicit permission to assess.
- Never use real passwords, API keys, session cookies, or other secrets in test requests.
- Review generated reports before sharing or publishing them.
- Do not assume that redaction removes every possible form of sensitive information.
- Do not use this tool as a substitute for a comprehensive security assessment.

## Limitations

- This is an HTTP request analysis tool, not a full web vulnerability scanner.
- Analysis results depend on the request supplied, the target server, and network conditions.
- HTTP status codes alone do not establish whether an application is secure.
- JSON parsing is applicable only when the response contains data that can be parsed as JSON.
- The tool does not guarantee that all sensitive information will be identified or redacted.

## Future Improvements

Potential improvements include:

- Additional request and response analysis features.
- Expanded automated test coverage.
- More configurable report formats.
- Improved command-line usability.
- Additional security-focused checks for authorized testing.

## Project Status

The core development and automated testing are in progress or undergoing final verification. Documentation, test coverage, and repository configuration may be updated as the project evolves.

## Author

**Mohit Pal**

## License

This project will be distributed under the license specified in the repository's `LICENSE` file.

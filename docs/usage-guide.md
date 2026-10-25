# HTTP Request Analyzer — Usage Guide

## 1. Overview

This guide explains how to set up and run HTTP Request Analyzer, provide request details, locate generated reports, and troubleshoot common issues.

Run the application only against systems you own or are authorized to test.

## 2. Prerequisites

- Python installed on the system.
- The project files available locally.
- Required Python dependencies installed from `requirements.txt`.
- Network connectivity when testing an external endpoint.

## 3. Open the Project

Open the project root directory in VS Code or navigate to it in PowerShell.

Example:

```powershell
Set-Location "D:\Mohit Pal Baghel\Domain\Ethical Hacking\EH Projects\http-request-analyzer"
```

The directory should contain `main.py`, `modules`, `tests`, and `requirements.txt`.

## 4. Activate the Virtual Environment

If the project virtual environment already exists, activate it in PowerShell:

```powershell
.\.vir_env\Scripts\Activate.ps1
```

The terminal prompt should show `(.vir_env)` when the environment is active.

If the environment does not exist, create it first:

```powershell
python -m venv .vir_env
```

Then activate it using the command above.

## 5. Install Dependencies

Install the dependencies listed in the project file:

```powershell
python -m pip install -r requirements.txt
```

Verify dependency consistency:

```powershell
python -m pip check
```

Expected result when dependencies are consistent:

```text
No broken requirements found.
```

## 6. Run the Application

From the project root directory, run:

```powershell
python main.py
```

Follow the interactive prompts. Supply the request details requested by the application.

Depending on the implementation, these details include the target URL, HTTP method, headers, request body, and timeout.

## 7. Input Guidelines

### URL

Use a valid HTTP or HTTPS URL for an endpoint you are authorized to test.

### HTTP Method

The project supports these methods:

- GET
- POST
- PUT
- DELETE

### Headers

Supply valid header information in the format requested by the CLI. Do not use real credentials, API keys, or session cookies for demonstration requests.

### JSON Request Body

When a request body is needed, provide valid JSON in the format expected by the application. The application validates JSON objects where required.

### Timeout

Supply a valid timeout value within the application's accepted range.

## 8. Understanding Results

The application may report:

- Request-analysis information.
- Response metadata.
- HTTP status interpretation.
- JSON parsing results when applicable.
- Request errors, such as timeouts or connection failures.
- A generated JSON report.

A successful HTTP exchange does not necessarily mean that the target application is functioning correctly or securely. An HTTP error status is still a response from the server.

## 9. Generated Reports

Reports are saved in the project's `reports/` directory according to the report generator's configuration.

Review the generated report before sharing it. Confirm that it contains no secrets or sensitive information.

Do not assume that redaction removes every possible sensitive value.

## 10. Run Automated Tests

From the project root, run:

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
```

A successful run ends with `OK`.

## 11. Troubleshooting

### ModuleNotFoundError

Check that the terminal is in the project root and that the virtual environment is activated. Install the dependencies if necessary.

### Connection Error

Check the target URL, network connection, DNS resolution, and whether the endpoint is reachable. Test only authorized endpoints.

### Request Timeout

The target server may be slow or unreachable. Check the configured timeout and retry only when appropriate.

### Invalid JSON

Check the syntax of the supplied JSON. Ensure that quotes, commas, brackets, and braces are correctly placed.

### Report Not Found

Check the `reports/` directory and inspect any error output from the application. Confirm the configured report output path.

### Mermaid Diagram Not Rendering

Open the Markdown preview in VS Code using `Ctrl + Shift + V`. If Mermaid is not supported by the preview environment, inspect the diagram source or use a Mermaid-compatible renderer.

## 12. Related Documentation

- [Architecture](architecture.md)
- [Workflow Diagram](workflow.md)
- [Project README](../README.md)

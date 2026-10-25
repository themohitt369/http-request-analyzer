# HTTP Request Analyzer — Testing Guide

## 1. Purpose

This document explains how to run the automated test suite and perform basic verification checks for HTTP Request Analyzer.

Automated tests help identify regressions and confirm that supported application behavior works as expected.

## 2. Test Location

The automated test suite is located at:

`tests/test_automated_suite.py`

The project uses Python's built-in `unittest` framework.

## 3. Prerequisites

Before running tests:

- Open the project root directory in VS Code.
- Activate the project's virtual environment.
- Install the project dependencies from `requirements.txt`.

Refer to the [Usage Guide](usage-guide.md) for setup instructions.

## 4. Run the Automated Test Suite

From the project root, run:

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
```

The command discovers matching test files inside `tests/` and runs them in verbose mode.

### Expected Result

A successful run ends with output similar to:

```text
Ran 44 tests in ...s

OK
```

The number of tests may change as the project evolves. The important success indicator is `OK`, with no failures or errors.

## 5. Compile-Time Syntax Check

Run:

```powershell
python -m compileall -q main.py modules tests
```

This checks Python files for syntax errors.

**Expected result:** no output when compilation succeeds. A syntax error produces diagnostic output.

## 6. Import Check

Run:

```powershell
python -c "import main; from modules import cli_handler, json_parser, report_generator, request_analyzer, request_sender, response_analyzer, security_utils, status_interpreter; print('All imports passed')"
```

**Expected result:**

```text
All imports passed
```

This checks whether the main module and listed modules can be imported in the current environment.

## 7. Dependency Consistency Check

Run:

```powershell
python -m pip check
```

**Expected result:**

```text
No broken requirements found.
```

This checks for incompatible or missing installed package requirements reported by pip.

## 8. Manual Verification

After automated checks, verify the application manually:

1. Run `python main.py`.
2. Enter valid request details using a permitted test endpoint.
3. Confirm the application handles the request and displays its analysis.
4. If report generation is supported for that run, inspect the generated report.
5. Test invalid input and confirm that the application responds appropriately.
6. Review generated files to ensure sensitive data is not unintentionally exposed.

Manual results depend on network access, the target endpoint, and the inputs provided.

## 9. Troubleshooting

### Tests fail to import a module

- Confirm that the terminal is in the project root.
- Confirm that the virtual environment is active.
- Check that the referenced module file exists.
- Read the complete traceback before changing code.

### A request test fails because of network access

A test involving a remote endpoint can fail because of connectivity, DNS, server availability, or timeout conditions. Determine whether the test is intended to use a controlled mock response or a live endpoint before diagnosing it as an application defect.

### Dependency check reports conflicts

Review the package names and version constraints in the output. Resolve dependency issues deliberately, then rerun the checks.

## 10. Test Scope and Limitations

Passing tests does not prove that the application is free from defects or that a target website is secure.

The test suite only checks the behaviors covered by its test cases. Network-dependent behavior, unusual server responses, and untested edge cases may require additional verification.

## 11. Related Documentation

- [Architecture](architecture.md)
- [Workflow Diagram](workflow.md)
- [Usage Guide](usage-guide.md)
- [Security and Limitations](security-and-limitations.md)
- [Project README](../README.md)

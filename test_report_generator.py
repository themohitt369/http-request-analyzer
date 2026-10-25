
import json
import tempfile
from pathlib import Path

from modules.report_generator import JSONReportGenerator


with tempfile.TemporaryDirectory() as temp_dir:
    generator = JSONReportGenerator(
        output_dir=Path(temp_dir) / "reports"
    )

    request_analysis = {
        "method": "GET",
        "url": "https://example.com/api",
        "headers": {
            "Authorization": "Bearer test-secret"
        },
    }

    response_analysis = {
        "status_code": 200,
        "content_type": "application/json",
        "response_size_bytes": 125,
        "elapsed_seconds": 0.25,
    }

    status_interpretation = {
        "status_code": 200,
        "category": "Success",
        "phrase": "OK",
    }

    json_parse_result = {
        "success": True,
        "data_type": "object",
        "item_count": 2,
    }

    output_path = generator.generate_and_save(
        request_analysis=request_analysis,
        response_analysis=response_analysis,
        status_interpretation=status_interpretation,
        json_parse_result=json_parse_result,
        filename="test_report.json",
    )

    assert output_path.exists()
    print("Test 1 passed: Report file created")

    with output_path.open("r", encoding="utf-8") as file:
        saved_report = json.load(file)

    assert saved_report["response_analysis"]["status_code"] == 200
    assert (
        saved_report["request_analysis"]["headers"]["Authorization"]
        == "[REDACTED]"
    )
    assert saved_report["report_metadata"]["report_version"] == "1.0"
    print("Test 2 passed: Report JSON and structure verified")

    report_text = output_path.read_text(encoding="utf-8")
    assert "test-secret" not in report_text
    print("Test 3 passed: Sensitive value not present in report")

    # Check that existing files are not overwritten.
    try:
        generator.save_report(
            saved_report,
            filename="test_report.json",
        )
    except FileExistsError:
        print("Test 4 passed: Existing report is protected")
    else:
        raise AssertionError("Expected FileExistsError")

    # Check that path traversal filenames are rejected.
    try:
        generator.save_report(
            saved_report,
            filename="../unsafe.json",
        )
    except ValueError:
        print("Test 5 passed: Unsafe filename rejected")
    else:
        raise AssertionError("Expected ValueError")

print("\nAll report generator tests passed.")

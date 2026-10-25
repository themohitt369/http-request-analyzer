import json
import unittest
from unittest.mock import Mock, patch
import tempfile
from pathlib import Path
from modules.report_generator import JSONReportGenerator

from modules.cli_handler import (
    validate_url,
    validate_method,
    validate_timeout,
    parse_json_object,
    validate_headers,
)
from modules.request_sender import RequestSender
from modules.status_interpreter import StatusCodeInterpreter
from modules.security_utils import SecurityUtils


class TestInputValidation(unittest.TestCase):

    def test_valid_url(self):
        self.assertEqual(
            validate_url("https://httpbin.org/get"),
            "https://httpbin.org/get",
        )

    def test_reject_ftp_url(self):
        with self.assertRaises(ValueError):
            validate_url("ftp://example.com")

    def test_valid_method_case_insensitive(self):
        self.assertEqual(validate_method("get"), "GET")

    def test_reject_unsupported_method(self):
        with self.assertRaises(ValueError):
            validate_method("TRACE")

    def test_valid_timeout(self):
        self.assertEqual(validate_timeout("10"), 10.0)

    def test_reject_invalid_timeout(self):
        with self.assertRaises(ValueError):
            validate_timeout("0")

    def test_parse_json_object(self):
        self.assertEqual(
            parse_json_object('{"name":"Test"}', "Body"),
            {"name": "Test"},
        )

    def test_reject_json_array_for_object(self):
        with self.assertRaises(ValueError):
            parse_json_object("[1, 2]", "Body")

    def test_reject_empty_url(self):
        with self.assertRaises(ValueError):
            validate_url("")

    def test_reject_url_without_hostname(self):
        with self.assertRaises(ValueError):
            validate_url("https://")

    def test_reject_url_with_credentials(self):
        with self.assertRaises(ValueError):
            validate_url("https://user:password@example.com")

    def test_reject_url_with_invalid_port(self):
        with self.assertRaises(ValueError):
            validate_url("https://example.com:abc")

    def test_reject_empty_method(self):
        with self.assertRaises(ValueError):
            validate_method("")

    def test_accept_maximum_timeout(self):
        self.assertEqual(validate_timeout("60"), 60.0)

    def test_reject_timeout_above_maximum(self):
        with self.assertRaises(ValueError):
            validate_timeout("61")

    def test_reject_non_numeric_timeout(self):
        with self.assertRaises(ValueError):
            validate_timeout("abc")

    def test_blank_json_returns_empty_object(self):
        self.assertEqual(parse_json_object("", "Body"), {})

    def test_reject_malformed_json(self):
        with self.assertRaises(ValueError):
            parse_json_object('{"name":}', "Body")

    def test_reject_json_string_for_object(self):
        with self.assertRaises(ValueError):
            parse_json_object('"hello"', "Body")

    def test_accept_valid_headers(self):
        headers = {"Accept": "application/json"}
        self.assertEqual(validate_headers(headers), headers)

    def test_reject_header_name_with_spaces(self):
        with self.assertRaises(ValueError):
            validate_headers({"Invalid Header": "value"})

    def test_reject_non_string_header_value(self):
        with self.assertRaises(ValueError):
            validate_headers({"Accept": 123})

    def test_reject_header_value_with_newline(self):
        with self.assertRaises(ValueError):
            validate_headers({"X-Test": "safe\r\nInjected: true"})


class TestRequestSender(unittest.TestCase):

    @patch("modules.request_sender.requests.Session")
    def test_http_404_is_a_successful_transport(self, session_class):
        session = session_class.return_value
        response = Mock()
        response.status_code = 404
        session.request.return_value = response

        sender = RequestSender()
        result = sender.send_request({
            "url": "https://example.com/missing",
            "method": "GET",
            "headers": {},
            "body": {},
            "timeout": 10.0,
        })

        self.assertTrue(result["success"])
        self.assertEqual(result["response"].status_code, 404)

    @patch("modules.request_sender.requests.Session")
    def test_timeout_is_handled(self, session_class):
        import requests

        session = session_class.return_value
        session.request.side_effect = requests.exceptions.Timeout()

        sender = RequestSender()
        result = sender.send_request({
            "url": "https://example.com/",
            "method": "GET",
            "headers": {},
            "body": {},
            "timeout": 1.0,
        })

        self.assertFalse(result["success"])
        self.assertEqual(result["error_type"], "Timeout")

    @patch("modules.request_sender.requests.Session")
    def test_http_200_response(self, session_class):
        session = session_class.return_value
        response = Mock()
        response.status_code = 200
        session.request.return_value = response

        sender = RequestSender()
        result = sender.send_request({
            "url": "https://example.com/",
            "method": "GET",
            "headers": {},
            "body": {},
            "timeout": 10.0,
        })

        self.assertTrue(result["success"])
        self.assertEqual(result["response"].status_code, 200)

    @patch("modules.request_sender.requests.Session")
    def test_http_500_is_a_successful_transport(self, session_class):
        session = session_class.return_value
        response = Mock()
        response.status_code = 500
        session.request.return_value = response

        sender = RequestSender()
        result = sender.send_request({
            "url": "https://example.com/",
            "method": "GET",
            "headers": {},
            "body": {},
            "timeout": 10.0,
        })

        self.assertTrue(result["success"])
        self.assertEqual(result["response"].status_code, 500)

    @patch("modules.request_sender.requests.Session")
    def test_connection_error_is_handled(self, session_class):
        import requests

        session = session_class.return_value
        session.request.side_effect = requests.exceptions.ConnectionError()

        sender = RequestSender()
        result = sender.send_request({
            "url": "https://example.com/",
            "method": "GET",
            "headers": {},
            "body": {},
            "timeout": 10.0,
        })

        self.assertFalse(result["success"])
        self.assertEqual(result["error_type"], "ConnectionError")

    @patch("modules.request_sender.requests.Session")
    def test_request_parameters_are_forwarded(self, session_class):
        session = session_class.return_value
        response = Mock()
        response.status_code = 200
        session.request.return_value = response

        sender = RequestSender()
        request_data = {
            "url": "https://example.com/",
            "method": "POST",
            "headers": {"Accept": "application/json"},
            "body": {"name": "Test"},
            "timeout": 5.0,
        }

        sender.send_request(request_data)

        session.request.assert_called_once_with(
            method="POST",
            url="https://example.com/",
            headers={"Accept": "application/json"},
            json={"name": "Test"},
            timeout=5.0,
            allow_redirects=False,
        )


class TestStatusInterpreter(unittest.TestCase):

    def test_404_is_client_error(self):
        result = StatusCodeInterpreter().interpret(404)
        self.assertEqual(result["category"], "Client Error")

    def test_reject_invalid_status(self):
        with self.assertRaises(ValueError):
            StatusCodeInterpreter().interpret(600)


class TestSecurityUtils(unittest.TestCase):

    def test_nested_token_is_redacted(self):
        security = SecurityUtils()
        result = security.redact_data({
            "config": {"access_token": "secret-value"}
        })

        self.assertEqual(
            result["config"]["access_token"],
            "[REDACTED]",
        )

    def test_original_data_is_not_modified(self):
        security = SecurityUtils()
        original = {"password": "test-password"}
        security.redact_data(original)

        self.assertEqual(original["password"], "test-password")

    def test_redact_password_field(self):
        security = SecurityUtils()
        result = security.redact_data({
            "password": "my-secret-password"
        })

        self.assertEqual(result["password"], "[REDACTED]")

    def test_redact_api_key_field(self):
        security = SecurityUtils()
        result = security.redact_data({
            "api_key": "my-secret-api-key"
        })

        self.assertEqual(result["api_key"], "[REDACTED]")

    def test_redact_multiple_nested_secrets(self):
        security = SecurityUtils()
        result = security.redact_data({
            "user": {
                "password": "secret-password",
                "access_token": "secret-token",
            },
            "api_key": "secret-api-key",
        })

        self.assertEqual(result["user"]["password"], "[REDACTED]")
        self.assertEqual(result["user"]["access_token"], "[REDACTED]")
        self.assertEqual(result["api_key"], "[REDACTED]")

    def test_redaction_preserves_non_sensitive_fields(self):
        security = SecurityUtils()
        result = security.redact_data({
            "username": "test-user",
            "status": "active",
            "password": "secret",
        })

        self.assertEqual(result["username"], "test-user")
        self.assertEqual(result["status"], "active")
        self.assertEqual(result["password"], "[REDACTED]")

    def test_json_round_trip(self):
        original = {
            "status": 200,
            "data": {"message": "success"},
        }

        encoded = json.dumps(original)
        decoded = json.loads(encoded)

        self.assertEqual(decoded, original)


class TestReportGenerator(unittest.TestCase):

    def test_generate_report_contains_expected_sections(self):
        generator = JSONReportGenerator()

        report = generator.generate_report(
            request_analysis={"url": "https://example.com/"},
            response_analysis={"status_code": 200},
            status_interpretation={"category": "Success"},
            json_parse_result={"is_json": True},
        )

        self.assertIn("report_metadata", report)
        self.assertIn("request_analysis", report)
        self.assertIn("response_analysis", report)
        self.assertIn("status_interpretation", report)
        self.assertIn("json_parse_result", report)
        self.assertIn("request_error", report)

    def test_generate_report_does_not_include_raw_response_body(self):
        generator = JSONReportGenerator()

        report = generator.generate_report(
            response_analysis={
                "status_code": 200,
                "content_type": "application/json",
            }
        )

        self.assertNotIn("response_body", report["response_analysis"])
        self.assertNotIn("raw_response_body", report["response_analysis"])

    def test_save_report_creates_valid_json_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            generator = JSONReportGenerator(output_dir=temp_dir)
            report = {
                "request_analysis": {"url": "https://example.com/"},
                "response_analysis": {"status_code": 200},
            }

            saved_path = generator.save_report(
                report,
                filename="test_report.json",
            )

            self.assertTrue(saved_path.exists())
            self.assertEqual(saved_path.name, "test_report.json")

            with saved_path.open("r", encoding="utf-8") as file:
                loaded_report = json.load(file)

            self.assertEqual(loaded_report["response_analysis"]["status_code"], 200)

    def test_save_report_redacts_sensitive_data(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            generator = JSONReportGenerator(output_dir=temp_dir)
            report = {
                "request_analysis": {
                    "headers": {"Authorization": "Bearer secret-token"}
                }
            }

            saved_path = generator.save_report(
                report,
                filename="safe_report.json",
            )

            with saved_path.open("r", encoding="utf-8") as file:
                loaded_report = json.load(file)

            self.assertEqual(
                loaded_report["request_analysis"]["headers"]["Authorization"],
                "[REDACTED]",
            )

    def test_save_report_rejects_invalid_filename(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            generator = JSONReportGenerator(output_dir=temp_dir)

            invalid_filenames = [
                "../outside.json",
                "folder/report.json",
                "report.txt",
                "",
            ]

            for filename in invalid_filenames:
                with self.subTest(filename=filename):
                    with self.assertRaises(ValueError):
                        generator.save_report({}, filename=filename)

    def test_save_report_rejects_non_dictionary(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            generator = JSONReportGenerator(output_dir=temp_dir)

            with self.assertRaises(TypeError):
                generator.save_report(["not", "a", "dictionary"])


if __name__ == "__main__":
    unittest.main()

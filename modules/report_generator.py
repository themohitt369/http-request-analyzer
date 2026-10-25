import json 
from datetime import datetime,timezone
from pathlib import Path
from modules.security_utils import SecurityUtils


class JSONReportGenerator:
    """ Build and save sanitized HTTP analysis reports. """

    def __init__(self,output_dir="reports"):
        self.output_dir=Path(output_dir)
        self.security=SecurityUtils()

    def generate_report(
            self,
            request_analysis=None,
            response_analysis=None,
            status_interpretation=None,
            json_parse_result=None,
            request_error=None,
    ):
        """ Create a structured report without including raw response bodies. """
        report={
            "report_metadata":{
                "generated_at":datetime.now(timezone.utc).isoformat(),
                "report_version":"1.0",
                "tool":"HTTP Request Analyzer",
            },
            "request_analysis":request_analysis or {},
            "response_analysis":response_analysis or {},
            "status_interpretation":status_interpretation or {},
            "json_parse_result":json_parse_result or {},
            "request_error":request_error,
        }

        # Recursively redact sensitive fields before saving.
        return self.security.redact_data(report)

    def save_report(self,report,filename=None):
        """ Save a report as JSON and return the saved file path. """

        if not isinstance(report,dict):
            raise TypeError("Report must be a dictionary.")
         # Sanitize again at the file-writing boundary.
        safe_report = self.security.redact_data(report)

        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            filename = f"http_report_{timestamp}.json"

        # Only allow a simple filename, not a path supplied by the caller.
        if (
            not isinstance(filename, str)
            or not filename
            or Path(filename).name != filename
            or filename in {".", ".."}
            or not filename.lower().endswith(".json")
        ):
            raise ValueError(
                "Filename must be a simple .json filename."
            )

        try:
            self.output_dir.mkdir(parents=True, exist_ok=True)
            output_path = self.output_dir / filename

            with output_path.open("x", encoding="utf-8") as file:
                json.dump(
                    safe_report,
                    file,
                    indent=4,
                    ensure_ascii=False,
                )
                file.write("\n")

            return output_path

        except FileExistsError:
            raise FileExistsError(
                "A report with this filename already exists."
            ) from None

        except OSError:
            raise OSError(
                "Could not save the report. Check the output directory "
                "and file permissions."
            ) from None

    def generate_and_save(
        self,
        request_analysis=None,
        response_analysis=None,
        status_interpretation=None,
        json_parse_result=None,
        request_error=None,
        filename=None,
    ):
        """Build a report, save it, and return its path."""

        report = self.generate_report(
            request_analysis=request_analysis,
            response_analysis=response_analysis,
            status_interpretation=status_interpretation,
            json_parse_result=json_parse_result,
            request_error=request_error,
        )

        return self.save_report(report, filename=filename)

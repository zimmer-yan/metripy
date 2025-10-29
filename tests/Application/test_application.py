from unittest import TestCase
from unittest.mock import MagicMock, patch

from metripy.Application.Application import Application


class TestApplicationRun(TestCase):
    @patch("metripy.Application.Application.CliOutput")
    @patch("metripy.Application.Application.Debugger")
    @patch("metripy.Application.Application.Parser")
    @patch("metripy.Application.Application.Finder")
    @patch("metripy.Application.Application.Analyzer")
    @patch("metripy.Application.Application.ReporterFactory")
    def test_run(
        self,
        mock_reporter_factory,
        mock_analyzer,
        mock_finder,
        mock_parser,
        mock_debugger,
        mock_cli_output,
    ):
        # Setup mocks
        mock_output = MagicMock()
        mock_cli_output.return_value = mock_output

        mock_debug = MagicMock()
        mock_debugger.return_value.enable.return_value = mock_debug

        mock_config = MagicMock()
        mock_project_config = MagicMock()
        mock_project_config.name = "TestProject"
        mock_project_config.reports = [MagicMock()]
        mock_config.project_configs = [mock_project_config]
        mock_parser.return_value.parse.return_value = mock_config
        mock_finder.return_value.fetch.return_value = {
            "TestProject": ["file1.py", "file2.py"]
        }

        mock_metrics = MagicMock()
        mock_analyzer.return_value.run.return_value = mock_metrics

        mock_reporter = MagicMock()
        mock_reporter_factory.create.return_value = mock_reporter

        # Run application
        app = Application()
        app.run(["--config", "test_config.yml"])

        # Assertions
        mock_output.writeln.assert_any_call(
            f"<info>Analying Project {mock_project_config.name}...</info>"
        )
        mock_output.writeln.assert_any_call(
            f"<success>Done analying Project {mock_project_config.name}</success>"
        )
        mock_output.writeln.assert_any_call(
            f"<info>Generating reports for {mock_project_config.name}...</info>"
        )
        mock_output.writeln.assert_any_call(
            f"<success>Reports generated for {mock_project_config.name}</success>"
        )
        mock_reporter.generate.assert_called_once_with(mock_metrics)

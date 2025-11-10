from unittest import TestCase
from unittest.mock import MagicMock, patch

from metripy.Application.Analyzer import Analyzer
from metripy.Dependency.Dependency import Dependency
from metripy.Metric.Code.FileMetrics import FileMetrics
from metripy.Metric.Git.GitMetrics import GitMetrics
from metripy.Metric.ProjectMetrics import ProjectMetrics


class TestAnalyzer(TestCase):
    def setUp(self):
        self.mock_config = MagicMock()
        self.mock_config.git = True
        self.mock_config.composer = False
        self.mock_config.pip = True
        self.mock_config.npm = False
        self.mock_config.base_path = "/mock/path"

        self.mock_output = MagicMock()
        self.mock_debugger = MagicMock()

        self.analyzer = Analyzer(self.mock_config, self.mock_output, self.mock_debugger)

    @patch("metripy.Application.Analyzer.GitAnalyzer")
    def test_analyze_git(self, mock_git_analyzer):
        mock_git_metrics = MagicMock(spec=GitMetrics)
        mock_git_analyzer.return_value.analyze.return_value = mock_git_metrics

        result = self.analyzer.analyze_git()
        self.assertEqual(result, mock_git_metrics)
        self.mock_output.writeln.assert_any_call(
            "<info>Analyzing git history...</info>"
        )
        self.mock_output.writeln.assert_any_call(
            "<success>Git history analyzed</success>"
        )

    @patch("metripy.Application.Analyzer.ProgressBar")
    def test_analyze_code(self, mock_progress_bar):
        mock_runner = MagicMock()
        mock_runner.is_needed.return_value = True
        mock_runner.get_metrics.return_value = [MagicMock(spec=FileMetrics)]
        self.analyzer.runners = [mock_runner]

        files = ["file1.py", "file2.py"]
        result = self.analyzer.analyze_code(files)
        self.assertEqual(len(result), 1)
        self.mock_output.writeln.assert_any_call("<info>Analyzing code...</info>")
        self.mock_output.writeln.assert_any_call("<success>Code analyzed</success>")

    @patch("metripy.Application.Analyzer.Composer")
    def test_analyze_composer(self, mock_composer):
        mock_dependencies = [MagicMock(spec=Dependency)]
        mock_composer.return_value.get_composer_dependencies.return_value = (
            mock_dependencies
        )
        result = self.analyzer.analyze_composer()
        self.assertEqual(result, mock_dependencies)
        self.mock_output.writeln.assert_any_call(
            "<info>Analyzing composer packages...</info>"
        )
        self.mock_output.writeln.assert_any_call(
            "<success>Composer packages analyzed</success>"
        )

    @patch("metripy.Application.Analyzer.Pip")
    def test_analyze_pip(self, mock_pip):
        mock_dependencies = [MagicMock(spec=Dependency)]
        mock_pip.return_value.get_dependencies.return_value = mock_dependencies

        result = self.analyzer.analyze_pip()
        self.assertEqual(result, mock_dependencies)
        self.mock_output.writeln.assert_any_call(
            "<info>Analyzing pip packages...</info>"
        )
        self.mock_output.writeln.assert_any_call(
            "<success>Pip packages analyzed</success>"
        )

    @patch("metripy.Application.Analyzer.Npm")
    def test_analyze_npm(self, mock_npm):
        mock_dependencies = [MagicMock(spec=Dependency)]
        mock_npm.return_value.get_dependencies.return_value = mock_dependencies

        result = self.analyzer.analyze_npm()
        self.assertEqual(result, mock_dependencies)
        self.mock_output.writeln.assert_any_call(
            "<info>Analyzing npm packages...</info>"
        )
        self.mock_output.writeln.assert_any_call(
            "<success>Npm packages analyzed</success>"
        )

    @patch.object(Analyzer, "add_trends")
    @patch.object(Analyzer, "analyze_git")
    @patch.object(Analyzer, "analyze_code")
    @patch.object(Analyzer, "analyze_pip")
    def test_run(
        self, mock_analyze_pip, mock_analyze_code, mock_analyze_git, mock_add_trends
    ):
        mock_git_metrics = MagicMock(spec=GitMetrics)
        mock_file_metric = MagicMock(spec=FileMetrics)
        mock_file_metric.loc = 123
        mock_file_metric.avgCcPerFunction = 12
        mock_file_metric.maintainabilityIndex = 89
        mock_file_metric.avgLocPerFunction = 10
        mock_file_metrics = [mock_file_metric]
        mock_dependencies = [MagicMock(spec=Dependency)]

        mock_analyze_git.return_value = mock_git_metrics
        mock_analyze_code.return_value = mock_file_metrics
        mock_analyze_pip.return_value = mock_dependencies
        # Mock add_trends to avoid trying to read historical data
        mock_add_trends.return_value = None

        files = ["file1.py", "file2.py"]
        result = self.analyzer.run(files)

        self.assertIsInstance(result, ProjectMetrics)
        self.assertEqual(result.git_metrics, mock_git_metrics)
        self.assertEqual(result.file_metrics, mock_file_metrics)
        self.assertEqual(result.dependencies, mock_dependencies)

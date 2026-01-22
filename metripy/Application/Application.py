import json

from metripy.Application.Analyzer import Analyzer
from metripy.Application.Config.Parser import Parser
from metripy.Application.Info import Info
from metripy.Component.Debug.Debugger import Debugger
from metripy.Component.File.Finder import Finder
from metripy.Component.Output.CliOutput import CliOutput
from metripy.Metric.ProjectMetrics import ProjectMetrics
from metripy.Report.ReporterFactory import ReporterFactory
from metripy.Report.ReporterInterface import ReporterInterface
from metripy.Report.Html.ProjectIndexRenderer import ProjectIndexRenderer
from metripy.Application.FailureEvaluator import FailureEvaluator


class Application:
    def run(self, argv) -> None:
        output = CliOutput()

        # issues and debug
        debugger = Debugger(output)

        config = Parser().parse(argv)
        if config.debug:
            debugger.enable()

        if config.version:
            output.writeln(Info().get_version_info())
            return

        if config.help:
            output.writeln(Info().get_help())
            return

        if config.quiet:
            output.set_quiet(True)

        finder = Finder()
        files = finder.fetch(config.project_configs)

        project_metrics_list: list[ProjectMetrics] = []
        # projectname, projectmetrics, htmlreportpath
        project_index_data: list[tuple[str, ProjectMetrics, str | None]] = []

        for project_config in config.project_configs:
            debugger.debug(project_config.name)
            project_files = files[project_config.name]
            debugger.debug(f"Found {len(project_files)} files")
            debugger.debug(json.dumps(project_files))

            output.writeln(f"<info>Analying Project {project_config.name}...</info>")
            project_metrics = Analyzer(project_config, output, debugger).run(
                project_files
            )
            project_metrics_list.append(project_metrics)
            output.writeln(
                f"<success>Done analying Project {project_config.name}</success>"
            )

            # Track HTML report path for this project
            html_report_path = None
            for report_config in project_config.reports:
                if report_config.type == "html":
                    html_report_path = report_config.path
                    break

            if not project_config.reports:
                output.writeln(
                    f"<success>Skipping reports of {project_config.name}!</success>"
                )
                project_index_data.append(
                    (project_config.name, project_metrics, html_report_path)
                )
                continue

            output.writeln(
                f"<info>Generating reports for {project_config.name}...</info>"
            )
            for report_config in project_config.reports:
                reporter: ReporterInterface = ReporterFactory.create(
                    report_config, output, project_config.name
                )
                reporter.generate(project_metrics)
            output.writeln(
                f"<success>Reports generated for {project_config.name}</success>"
            )

            project_index_data.append(
                (project_config.name, project_metrics, html_report_path)
            )

        # Generate HTML index page if configured
        if config.html_index:
            output.writeln("<info>Generating HTML project index...</info>")
            index_renderer = ProjectIndexRenderer(config.html_index)
            index_renderer.render(project_index_data)
            output.writeln(
                f"<success>HTML project index generated: {config.html_index}</success>"
            )

        exit_code = FailureEvaluator(config.failure, output).get_exit_code(
            project_metrics_list
        )

        exit(exit_code)

import json
import os
import shutil
from datetime import datetime

from py_template_engine import TemplateEngine

from metripy.Application.Config.ReportConfig import ReportConfig
from metripy.Component.Output.CliOutput import CliOutput
from metripy.Dependency.Dependency import Dependency
from metripy.Metric.FileTree.FileTreeParser import FileTreeParser
from metripy.Metric.ProjectMetrics import ProjectMetrics
from metripy.Report.ReporterInterface import ReporterInterface


class Reporter(ReporterInterface):
    def __init__(
        self, config: ReportConfig, output: CliOutput, project_name: str = "foobar"
    ):
        self.config: ReportConfig = config
        self.output = output
        self.template_dir = os.path.join(os.getcwd(), "templates/html_report")

        self.global_template_args = {
            "project_name": project_name,
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

    def generate(self, metrics: ProjectMetrics):

        self.output.writeln("<info>Generating HTML report...</info>")

        # copy sources
        if not os.path.exists(os.path.join(self.config.path, "js")):
            os.makedirs(os.path.join(self.config.path, "js"))
        if not os.path.exists(os.path.join(self.config.path, "css")):
            os.makedirs(os.path.join(self.config.path, "css"))
        if not os.path.exists(os.path.join(self.config.path, "images")):
            os.makedirs(os.path.join(self.config.path, "images"))
        if not os.path.exists(os.path.join(self.config.path, "fonts")):
            os.makedirs(os.path.join(self.config.path, "fonts"))
        if not os.path.exists(os.path.join(self.config.path, "data")):
            os.makedirs(os.path.join(self.config.path, "data"))

        # shutil.copy(os.path.join(self.template_dir, "favicon.ico"), os.path.join(self.config.path, "favicon.ico"))

        shutil.copytree(
            os.path.join(self.template_dir, "js"),
            os.path.join(self.config.path, "js"),
            dirs_exist_ok=True,
        )
        shutil.copytree(
            os.path.join(self.template_dir, "css"),
            os.path.join(self.config.path, "css"),
            dirs_exist_ok=True,
        )
        # shutil.copytree(os.path.join(self.template_dir, "images"), os.path.join(self.config.path, "images"), dirs_exist_ok=True)
        # shutil.copytree(os.path.join(self.template_dir, "fonts"), os.path.join(self.config.path, "fonts"), dirs_exist_ok=True)

        # render templates
        git_stats_data = {}
        if metrics.git_metrics:
            git_stats_data = metrics.git_metrics.get_commit_stats_per_month()

        self.output.writeln("<info>Rendering index page</info>")
        # Render main index page
        self.render_template(
            "index.html",
            {
                "git_stats_data": json.dumps(git_stats_data, indent=4),
                "total_code_metrics": metrics.total_code_metrics.to_dict(),
                "segmentation_data": json.dumps(
                    metrics.total_code_metrics.to_dict_segmentation(), indent=4
                ),
                "project_name": "Metripy",
                "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "author": "Metripy",
                "version": "1.0.0",
            },
        )
        self.output.writeln("<success>Done rendering index page</success>")

        # Render files page
        self.render_files_page(metrics)
        # Render git analysis page
        self.render_git_analysis_page(metrics)

        self.render_dependencies_page(metrics)

        self.render_top_offenders_page(metrics)

        self.output.writeln(
            f"<success>HTML report generated in {self.config.path} directory</success>"
        )

    def render_template(self, template_name: str, data: dict) -> str:
        engine = TemplateEngine(os.path.join(self.template_dir, template_name))
        content = engine.render(**data)
        with open(os.path.join(self.config.path, template_name), "w") as file:
            file.write(content)

    def render_top_offenders_page(self, metrics: ProjectMetrics):
        self.output.writeln("<info>Rendering top offenders page</info>")

        orderedByTotalCc = sorted(
            metrics.file_metrics, key=lambda x: x.totalCc, reverse=True
        )[:10]
        orderedByMI = sorted(
            metrics.file_metrics, key=lambda x: x.maintainabilityIndex, reverse=False
        )[:10]
        orderedByLoc = sorted(metrics.file_metrics, key=lambda x: x.loc, reverse=True)[
            :10
        ]

        all_functions: list = []
        for fm in metrics.file_metrics:
            # if fm.full_name == "./metripy/LangAnalyzer/AbstractLangAnalyzer.py":
            #    print([x.to_dict() for x in fm.function_nodes])
            #    exit()
            all_functions.extend(fm.function_nodes)

        functionsOrderedByCc = sorted(
            all_functions, key=lambda x: x.complexity, reverse=True
        )[:10]
        functionsOrderedByMi = sorted(
            all_functions, key=lambda x: x.maintainability_index, reverse=False
        )[:10]
        functionsOrderedByLoc = sorted(
            all_functions, key=lambda x: x.get_loc(), reverse=True
        )[:10]

        # TODO maintainability index per function, we dont calc yet

        a = {
            "bar": [x.to_dict() for x in functionsOrderedByCc],
            "baz": list(set([x.h1 for x in functionsOrderedByCc])),
            "soos": list(set([x.maintainability_index for x in functionsOrderedByMi])),
            "ff": [x.to_dict() for x in all_functions],
            "loc": [x.loc for x in orderedByLoc],
            "m_loc": [x.get_loc() for x in functionsOrderedByLoc],
            # "foo": [{"full_name": x.full_name, "totalCc": x.totalCc} for x in orderedByTotalCc]
        }

        print(json.dumps(a, indent=2))

        def get_cc_status(cc: int) -> str:
            if cc <= 5:
                return "good"
            if cc <= 10:
                return "ok"
            if cc <= 15:
                return "warning"
            return "critical"

        def get_mi_status(mi: int) -> str:
            if mi > 80:
                return "good"
            if mi > 60:
                return "ok"
            if mi > 40:
                return "warning"
            return "critical"

        def get_file_loc_status(loc: int) -> str:
            if loc <= 200:
                return "good"
            elif loc <= 500:
                return "ok"
            elif loc <= 1000:
                return "warning"
            else:
                return "critical"

        def get_method_size_status(loc: int) -> str:
            if loc <= 15:
                return "good"
            elif loc <= 30:
                return "ok"
            elif loc <= 50:
                return "warning"
            else:
                return "critical"

        self.render_template(
            "top_offenders.html",
            Reporter._stringify_values(
                {
                    "file_loc_offenders": [
                        {**e.to_dict(), "status": get_file_loc_status(e.loc)}
                        for e in orderedByLoc
                    ],
                    "file_cc_offenders": [
                        {**e.to_dict(), "status": get_cc_status(e.totalCc)}
                        for e in orderedByTotalCc
                    ],
                    "file_mi_offenders": [
                        {**e.to_dict(), "status": get_mi_status(e.maintainabilityIndex)}
                        for e in orderedByMI
                    ],
                    "function_size_offenders": [
                        {**e.to_dict(), "status": get_method_size_status(e.get_loc())}
                        for e in functionsOrderedByLoc
                    ],
                    "function_cc_offenders": [
                        {**e.to_dict(), "status": get_cc_status(e.complexity)}
                        for e in functionsOrderedByCc
                    ],  # [e.to_dict() for e in functionsOrderedByCc],#[{**e.to_dict(), "status": get_cc_status(e.complexity)} for e in functionsOrderedByCc],
                    "function_mi_offenders": [
                        {
                            **e.to_dict(),
                            "status": get_mi_status(e.maintainability_index),
                        }
                        for e in functionsOrderedByMi
                    ],
                    "project_name": "Metripy",
                    "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }
            ),
        )
        self.output.writeln(
            "<success>Top offenders page generated successfully</success>"
        )

    def render_dependencies_page(self, metrics: ProjectMetrics):
        """Render the dependencies page with dependency details and stats"""
        if not metrics.dependencies:
            self.output.writeln("<success>No dependencies to render</success>")
            return

        self.output.writeln("<info>Rendering dependencies page</info>")

        dependencies = metrics.dependencies if metrics.dependencies is not None else []

        # TODO render a pie chart
        license_by_type = Dependency.get_lisence_distribution(dependencies)

        print(json.dumps(license_by_type, indent=2))

        self.render_template(
            "dependencies.html",
            {
                "dependencies": [d.to_dict() for d in dependencies],
                "project_name": "Metripy",
                "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            },
        )
        self.output.writeln(
            "<success>Dependencies page generated successfully</success>"
        )

    def render_files_page(self, metrics: ProjectMetrics):
        """Render the files page with file details and analysis"""
        self.output.writeln("<info>Rendering files page</info>")

        file_names = []
        file_details = {}
        for file_metrics in metrics.file_metrics:
            file_name = file_metrics.full_name
            file_details[file_name] = file_metrics.to_dict()
            file_names.append(file_name)

        filetree = FileTreeParser.parse(file_names, shorten=True)

        self.render_template(
            "files.html",
            {
                "filetree": json.dumps(filetree.to_dict()),
                "file_details": json.dumps(file_details),
                "project_name": "Metripy",
                "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            },
        )
        self.output.writeln("<success>Files page generated successfully</success>")

    @staticmethod
    def _stringify_values(obj):
        if isinstance(obj, dict):
            return {
                key: Reporter._stringify_values(value) for key, value in obj.items()
            }
        elif isinstance(obj, list):
            return [Reporter._stringify_values(item) for item in obj]
        else:
            return str(obj)

    def render_git_analysis_page(self, metrics: ProjectMetrics):
        """Render the git analysis page with comprehensive git data"""
        if not metrics.git_metrics:
            self.output.writeln("<success>No git metrics to render</success>")
            return

        self.output.writeln("<info>Rendering git analysis page</info>")
        try:
            # Render git analysis template
            self.render_template(
                "git_analysis.html",
                Reporter._stringify_values(
                    {
                        "git_analysis": metrics.git_metrics.to_dict(),
                        "git_analysis_json": json.dumps(
                            metrics.git_metrics.get_contributors_dict(), indent=4
                        ),
                        "git_stats_data": json.dumps(
                            metrics.git_metrics.get_commit_stats_per_month(), indent=4
                        ),  # git commit graph
                        "git_churn_data": json.dumps(
                            metrics.git_metrics.get_churn_per_month(), indent=4
                        ),  # git chrun graph
                        "git_silos_data": metrics.git_metrics.get_silos_list()[
                            :10
                        ],  # silos list
                        "git_contributors": metrics.git_metrics.get_contributors_list()[
                            :10
                        ],  # contributors list
                        "git_hotspots_data": metrics.git_metrics.get_hotspots_list()[
                            :10
                        ],  # hotspots list
                        "project_name": "Metripy",
                        "last_updated": metrics.git_metrics.get_analysis_start_date(),
                    }
                ),
            )

            self.output.writeln(
                "<success>Git analysis page generated successfully</success>"
            )
        except Exception as e:
            raise e
            self.output.writeln(
                f"<error>Error generating git analysis page: {e}</error>"
            )

from metripy.Application.Config.ProjectConfig import ProjectConfig
from metripy.Component.Debug.Debugger import Debugger
from metripy.Component.Output.CliOutput import CliOutput
from metripy.Component.Output.ProgressBar import ProgressBar
from metripy.Dependency.Composer.Composer import Composer
from metripy.Dependency.Dependency import Dependency
from metripy.Dependency.Npm.Npm import Npm
from metripy.Dependency.Pip.Pip import Pip
from metripy.Git.GitAnalyzer import GitAnalyzer
from metripy.LangAnalyzer.AbstractLangAnalyzer import AbstractLangAnalyzer
from metripy.LangAnalyzer.Php.PhpAnalyzer import PhpAnalyzer
from metripy.LangAnalyzer.Python.PythonAnalyzer import PythonAnalyzer
from metripy.LangAnalyzer.Typescript.TypescriptAnalyzer import TypescriptAnalyzer
from metripy.Metric.Code.FileMetrics import FileMetrics
from metripy.Metric.Git.GitMetrics import GitMetrics
from metripy.Metric.ProjectMetrics import ProjectMetrics


class Analyzer:
    def __init__(self, config: ProjectConfig, output: CliOutput, debugger: Debugger):
        self.config = config
        self.output = output
        self.debugger = debugger
        self.runners: list[AbstractLangAnalyzer] = [
            PythonAnalyzer(),
            PhpAnalyzer(),
            TypescriptAnalyzer(),
        ]

    def analyze_git(self) -> GitMetrics:
        self.output.writeln("<info>Analyzing git history...</info>")
        metrics = GitAnalyzer(self.config.git).analyze()
        self.output.writeln("<success>Git history analyzed</success>")

        return metrics

    def analyze_code(self, files: list[str]) -> list[FileMetrics]:
        file_metrics = []

        # for multi language projects, register runner per language
        runner_sizes = []
        for runner in self.runners:
            runner.set_files(files)
            if not runner.is_needed():
                continue
            runner_sizes.append(len(runner.files))

        self.debugger.debug(len(files))
        self.output.writeln("<info>Analyzing code...</info>")
        progress_bar = ProgressBar(self.output, sum(runner_sizes))
        for runner in self.runners:
            if not runner.is_needed():
                continue
            runner.before_run()
            runner.run(progress_bar)
            runner.after_run()

            for metric in runner.get_metrics():
                file_metrics.append(metric)

        self.output.writeln("")
        self.output.writeln("<success>Code analyzed</success>")

        return file_metrics

    def analyze_composer(self) -> list[Dependency]:
        self.output.writeln("<info>Analyzing composer packages...</info>")
        dependencies = Composer().get_composer_dependencies(self.config.base_path)
        self.output.writeln("<success>Composer packages analyzed</success>")

        return dependencies

    def analyze_pip(self) -> list[Dependency]:
        self.output.writeln("<info>Analyzing pip packages...</info>")
        dependencies = Pip().get_dependencies(self.config.base_path)
        self.output.writeln("<success>Pip packages analyzed</success>")

        return dependencies

    def analyze_npm(self) -> list[Dependency]:
        self.output.writeln("<info>Analyzing npm packages...</info>")
        dependencies = Npm().get_dependencies(self.config.base_path)
        self.output.writeln("<success>Npm packages analyzed</success>")

        return dependencies

    def run(self, files: list[str]) -> ProjectMetrics:
        git_stats = None
        if self.config.git:
            git_stats = self.analyze_git()

        file_metrics = []
        if True:
            file_metrics = self.analyze_code(files)

        # TODO: analyze dependencies: composer, pip, npm, etc etc
        packages = None
        if self.config.composer:
            packages = self.analyze_composer()
        elif self.config.pip:
            packages = self.analyze_pip()
        elif self.config.npm:
            packages = self.analyze_npm()

        return ProjectMetrics(file_metrics, git_stats, packages)

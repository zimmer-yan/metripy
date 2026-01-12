from metripy.Application.Config.ReportConfig import ReportConfig
from metripy.Component.Output.CliOutput import CliOutput
from metripy.Metric.ProjectMetrics import ProjectMetrics
from metripy.Report.Json.AbstractJsonReporter import AbstractJsonReporter
from metripy.Metric.Code.Segmentor import Segmentor

class GlCodequalityReporter(AbstractJsonReporter):
    def __init__(self, config: ReportConfig, output: CliOutput):
        self.config = config
        self.output = output

    def generate(self, metrics: ProjectMetrics):
        self.put_data(self.transform_metrics(metrics))
        self.output.writeln(
            f"<success>Create gl-codequality-report in {self.config.path}</success>"
        )

    def transform_metrics(self, metrics: ProjectMetrics) -> list[dict]:
        items = []
        for file_metric in metrics.file_metrics:
            for function_node in file_metric.function_nodes:
                checks = [
                    ("Method size", "is too large", "method_size", "loc",
                     Segmentor.get_method_size_segment, function_node.get_loc()),
                    ("Cyclomatic complexity", "is too high", "cyclomatic_complexity", "cc",
                     Segmentor.get_complexity_segment, function_node.complexity),
                    ("Maintainability index", "is too low", "maintainability_index", "mi",
                     Segmentor.get_maintainability_segment, function_node.maintainability_index),
                    ("Cognitive complexity", "is too high", "cognitive_complexity", "cog_complexity",
                     Segmentor.get_complexity_segment, function_node.cognitive_complexity),
                ]
                for label, issue, check_name, fp_key, segment_fn, value in checks:
                    severity = self.segment_to_severity(segment_fn(value))
                    if not severity:
                        continue
                    items.append({
                        "description": f"{label} of {function_node.name} {issue}",
                        "check_name": check_name,
                        "fingerprint": hash(f"{function_node.full_name}_{fp_key}_{value}"),
                        "location": {
                            "path": file_metric.full_name,
                            "lines": {
                                "begin": function_node.lineno,
                            },
                        },
                        "severity": severity,
                    })
        return items

    def segment_to_severity(self, segment: str) -> str|None:
        if segment == "ok":
            return "minor"
        elif segment == "warning":
            return "major"
        elif segment == "critical":
            return "critical"
        return None

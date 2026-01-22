from metripy.Application.Config.FailureConfig import FailureConfig
from metripy.Metric.ProjectMetrics import ProjectMetrics
from metripy.Metric.Code.Segmentor import Segmentor
from collections import defaultdict
from metripy.Component.Output.CliOutput import CliOutput


class FailureEvaluator:
    def __init__(self, failure: dict[int, list[FailureConfig]], output: CliOutput):
        self.failure = failure
        self.output = output

    def get_exit_code(self, project_metrics_list: list[ProjectMetrics]) -> int:
        if not self.failure:
            return 0

        statistics = self.get_statistics(project_metrics_list)

        # we check all conditions and error out all of the info before exiting
        exit_codes = [0]
        for exit_code, failures in sorted(self.failure.items(), reverse=True):
            for failure in failures:
                if statistics[failure.value][failure.severity] >= failure.amount:
                    self.output.writeln(
                        f"<error>Failure condition met: {failure.value} has {statistics[failure.value][failure.severity]}/{failure.amount} of severity {failure.severity}</error>"
                    )
                    exit_codes.append(exit_code)

        return max(exit_codes)

    def get_statistics(
        self, project_metrics_list: list[ProjectMetrics]
    ) -> dict[str, dict[str, int]]:
        statistics: dict[str, dict[str, int]] = {
            "file_loc": defaultdict(int),
            "file_cyclomatic_complexity": defaultdict(int),
            "file_maintainability_index": defaultdict(int),
            "file_cognitive_complexity": defaultdict(int),
            "class_loc": defaultdict(int),
            "class_cyclomatic_complexity": defaultdict(int),
            "class_lcom4": defaultdict(int),
            "function_loc": defaultdict(int),
            "function_cyclomatic_complexity": defaultdict(int),
            "function_maintainability_index": defaultdict(int),
            "function_cognitive_complexity": defaultdict(int),
        }
        for project_metrics in project_metrics_list:
            for file_metrics in project_metrics.file_metrics:

                loc_segment = Segmentor.get_loc_segment(file_metrics.loc)
                complexity_segment = Segmentor.get_complexity_segment(
                    file_metrics.avgCcPerFunction
                )
                maintainability_segment = Segmentor.get_maintainability_segment(
                    file_metrics.maintainabilityIndex
                )
                cognitive_complexity_segment = Segmentor.get_complexity_segment(
                    file_metrics.avg_cog_complexity_per_function
                )

                statistics["file_loc"][loc_segment] += 1
                statistics["file_cyclomatic_complexity"][complexity_segment] += 1
                statistics["file_maintainability_index"][maintainability_segment] += 1
                statistics["file_cognitive_complexity"][
                    cognitive_complexity_segment
                ] += 1

                for class_node in file_metrics.class_nodes:
                    loc_segment = Segmentor.get_loc_segment(class_node.get_loc())
                    complexity_segment = Segmentor.get_complexity_segment(
                        class_node.real_complexity
                    )
                    lcom4_segment = Segmentor.get_lcom4_segment(class_node.lcom4)

                    statistics["class_loc"][loc_segment] += 1
                    statistics["class_cyclomatic_complexity"][complexity_segment] += 1
                    statistics["class_lcom4"][lcom4_segment] += 1

                for function_node in file_metrics.function_nodes:
                    loc_segment = Segmentor.get_loc_segment(function_node.get_loc())
                    complexity_segment = Segmentor.get_complexity_segment(
                        function_node.complexity
                    )
                    maintainability_segment = Segmentor.get_maintainability_segment(
                        function_node.maintainability_index
                    )
                    cognitive_complexity_segment = Segmentor.get_complexity_segment(
                        function_node.cognitive_complexity
                    )

                    statistics["function_loc"][loc_segment] += 1
                    statistics["function_cyclomatic_complexity"][
                        complexity_segment
                    ] += 1
                    statistics["function_maintainability_index"][
                        maintainability_segment
                    ] += 1
                    statistics["function_cognitive_complexity"][
                        cognitive_complexity_segment
                    ] += 1

        return statistics

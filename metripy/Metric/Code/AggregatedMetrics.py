from metripy.Metric.Code.SegmentedMetrics import SegmentedMetrics


class AggregatedMetrics:
    """Used to show aggregated metrics on the index page"""

    def __init__(
        self,
        loc: int = 0,
        avgCcPerFunction: float = 0.0,
        maintainabilityIndex: float = 0.0,
        avgLocPerFunction: float = 0.0,
        num_files: int = 0,
        segmented_loc: SegmentedMetrics = SegmentedMetrics(),
        segmented_complexity: SegmentedMetrics = SegmentedMetrics(),
        segmented_maintainability: SegmentedMetrics = SegmentedMetrics(),
        segmented_method_size: SegmentedMetrics = SegmentedMetrics(),
    ) -> None:
        self.loc = loc
        self.avgCcPerFunction = avgCcPerFunction
        self.maintainabilityIndex = maintainabilityIndex
        self.avgLocPerFunction = avgLocPerFunction
        self.num_files = num_files

        self.segmentation_data = {
            "loc": segmented_loc,
            "complexity": segmented_complexity,
            "maintainability": segmented_maintainability,
            "methodSize": segmented_method_size,
        }

    def to_dict(self) -> dict:
        return {
            "loc": str(self.loc),
            "avgCcPerFunction": f"{self.avgCcPerFunction:.2f}",
            "maintainabilityIndex": f"{self.maintainabilityIndex:.2f}",
            "avgLocPerFunction": f"{self.avgLocPerFunction:.2f}",
            "num_files": str(self.num_files),
        }

    def to_dict_segmentation(self) -> dict:
        return {k: v.to_dict() for k, v in self.segmentation_data.items()}

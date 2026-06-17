from metripy.Metric.Code.SegmentedMetrics import SegmentedMetrics


def test_to_dict_with_percent_returns_zero_percentages_for_empty_segments():
    assert SegmentedMetrics().to_dict_with_percent() == {
        "good": 0,
        "good_percent": 0,
        "ok": 0,
        "ok_percent": 0,
        "warning": 0,
        "warning_percent": 0,
        "critical": 0,
        "critical_percent": 0,
    }

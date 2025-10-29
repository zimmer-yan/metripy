from typing import Self


class SegmentedMetrics:
    def __init__(self):
        self.good = 0
        self.ok = 0
        self.warning = 0
        self.critical = 0

    def to_dict(self) -> dict:
        return {
            "good": self.good,
            "ok": self.ok,
            "warning": self.warning,
            "critical": self.critical,
        }

    def set_loc(self, values: list[int]) -> Self:
        for value in values:
            if value <= 200:
                self.good += 1
            elif value <= 500:
                self.ok += 1
            elif value <= 1000:
                self.warning += 1
            else:
                self.critical += 1
        return self

    def set_complexity(self, values: list[int]) -> Self:
        for value in values:
            if value <= 5:
                self.good += 1
            elif value <= 10:
                self.ok += 1
            elif value <= 20:
                self.warning += 1
            else:
                self.critical += 1
        return self

    def set_maintainability(self, values: list[int]) -> Self:
        for value in values:
            if value <= 80:
                self.critical += 1
            elif value <= 60:
                self.warning += 1
            elif value <= 40:
                self.ok += 1
            else:
                self.good += 1
        return self

    def set_method_size(self, values: list[int]) -> Self:
        for value in values:
            if value <= 15:
                self.good += 1
            elif value <= 30:
                self.ok += 1
            elif value <= 50:
                self.warning += 1
            else:
                self.critical += 1
        return self

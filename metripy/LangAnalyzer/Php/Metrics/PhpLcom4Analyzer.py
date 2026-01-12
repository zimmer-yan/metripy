from metripy.LangAnalyzer.Generic.Metrics.GenericLcom4Analyzer import (
    GenericLcom4Analyzer,
)


class PhpLcom4Analyzer(GenericLcom4Analyzer):
    def get_methods_to_ignore(self) -> list[str]:
        return [
            "__construct",
            "__destruct",
            "__clone",
            "__sleep",
            "__wakeup",
            "__toString",
            "__invoke",
            "__set",
            "__get",
            "__set_state",
            "__clone",
            "__debugInfo",
        ]

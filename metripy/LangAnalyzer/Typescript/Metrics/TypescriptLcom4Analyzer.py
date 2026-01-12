from metripy.LangAnalyzer.Generic.Metrics.GenericLcom4Analyzer import GenericLcom4Analyzer

class TypescriptLcom4Analyzer(GenericLcom4Analyzer):
    def get_methods_to_ignore(self) -> list[str]:
        return ["constructor"]

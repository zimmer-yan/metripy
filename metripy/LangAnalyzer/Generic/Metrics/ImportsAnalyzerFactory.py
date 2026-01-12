from metripy.LangAnalyzer.Generic.Metrics.GenericImportsAnalyzer import (
    GenericImportsAnalyzer,
)
from metripy.LangAnalyzer.Python.PythonImportsAnalyzer import PythonImportsAnalyzer
from metripy.LangAnalyzer.Php.PhpImportsAnalyzer import PhpImportsAnalyzer
from metripy.LangAnalyzer.Typescript.TypescriptImportsAnalyzer import TypescriptImportsAnalyzer

class ImportsAnalyzerFactory:
    _ANALYZERS = {
        "Python": PythonImportsAnalyzer(),
        "PHP": PhpImportsAnalyzer(),
        "Typescript": TypescriptImportsAnalyzer(),
    }

    @staticmethod
    def get_imports_analyzer(language: str) -> GenericImportsAnalyzer:
        try:
            return ImportsAnalyzerFactory._ANALYZERS[language]
        except KeyError:
            raise ValueError(f"No imports analyzer found for language: {language}")

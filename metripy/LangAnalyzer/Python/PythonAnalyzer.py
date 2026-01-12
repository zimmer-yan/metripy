from metripy.LangAnalyzer.AbstractLangAnalyzer import AbstractLangAnalyzer


class PythonAnalyzer(AbstractLangAnalyzer):
    def get_lang_name(self) -> str:
        return "Python"

    def get_supported_extensions(self) -> tuple[str]:
        return (".py",)

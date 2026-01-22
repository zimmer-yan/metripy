from metripy.LangAnalyzer.AbstractLangAnalyzer import AbstractLangAnalyzer


class TypescriptAnalyzer(AbstractLangAnalyzer):
    def get_lang_name(self) -> str:
        return "Typescript"

    def get_supported_extensions(self) -> tuple[str]:
        return (".ts", ".js")

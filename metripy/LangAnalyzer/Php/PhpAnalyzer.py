from metripy.LangAnalyzer.AbstractLangAnalyzer import AbstractLangAnalyzer

class PhpAnalyzer(AbstractLangAnalyzer):
    def get_lang_name(self) -> str:
        return "PHP"

    def get_supported_extensions(self) -> tuple[str]:
        return (".php",)

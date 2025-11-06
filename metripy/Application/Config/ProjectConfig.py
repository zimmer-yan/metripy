from metripy.Application.Config.GitConfig import GitConfig
from metripy.Application.Config.ReportConfig import ReportConfig


class ProjectConfig:
    def __init__(self, name: str):
        self.name: str = name
        self.base_path: str = "./"
        self.includes: list[str] = []
        self.excludes: list[str] = []
        self.extensions: list[str] = []
        self.git: GitConfig | None = None
        self.composer: bool = False
        self.pip: bool = False
        self.npm: bool = False
        self.reports: list[ReportConfig] = []
        self.history_path: str | None = None

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "base_path": self.base_path,
            "includes": self.includes,
            "excludes": self.excludes,
            "extensions": self.extensions,
            "git": self.git.to_dict() if self.git else None,
            "reports": [report.to_dict() for report in self.reports],
            "history_path": self.history_path,
        }

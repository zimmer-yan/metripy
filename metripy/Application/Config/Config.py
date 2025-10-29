from metripy.Application.Config.ProjectConfig import ProjectConfig


class Config:
    def __init__(self):
        self.project_configs: list[ProjectConfig] = []

    def to_dict(self) -> dict:
        return {
            "project_configs": [
                project_config.to_dict() for project_config in self.project_configs
            ],
        }

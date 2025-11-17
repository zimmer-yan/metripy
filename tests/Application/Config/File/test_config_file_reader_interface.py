from unittest import TestCase

from metripy.Application.Config.CodeSmellConfig import CodeSmellConfig
from metripy.Application.Config.Config import Config
from metripy.Application.Config.File.ConfigFileReaderInterface import (
    ConfigFileReaderInterface,
)
from metripy.Application.Config.ReportConfig import ReportConfig


class DummyConfigFileReaderInterface(ConfigFileReaderInterface):
    def read(self, config: Config) -> None:
        pass


class TestConfigFileReaderInterface(TestCase):

    def setUp(self):
        self.reader = DummyConfigFileReaderInterface("test.json")

    def test_parse_config_json_base_path(self):
        data = {"base_path": "test"}
        project_config = self.reader.parse_config_json("test", data)
        self.assertEqual(project_config.base_path, "test")

    def test_parse_config_json_includes(self):
        data = {"includes": ["test"]}
        project_config = self.reader.parse_config_json("test", data)
        self.assertEqual(project_config.includes, ["test"])

    def test_parse_config_json_extensions(self):
        data = {"extensions": ["test"]}
        project_config = self.reader.parse_config_json("test", data)
        self.assertEqual(project_config.extensions, ["test"])

    def test_parse_config_json_excludes(self):
        data = {"excludes": ["test"]}
        project_config = self.reader.parse_config_json("test", data)
        self.assertEqual(project_config.excludes, ["test"])

    def test_parse_config_json_reports(self):
        data = {"reports": {"html": "test"}}
        project_config = self.reader.parse_config_json("test", data)
        self.assertEqual(
            [x.to_dict() for x in project_config.reports],
            [ReportConfig("html", "test").to_dict()],
        )

    def test_parse_config_json_git(self):
        data = {"git": {"branch": "test"}}
        project_config = self.reader.parse_config_json("test", data)
        self.assertEqual(project_config.git.branch, "test")

    def test_parse_config_json_composer(self):
        data = {"composer": True}
        project_config = self.reader.parse_config_json("test", data)
        self.assertEqual(project_config.composer, True)

    def test_parse_config_json_pip(self):
        data = {"pip": True}
        project_config = self.reader.parse_config_json("test", data)
        self.assertEqual(project_config.pip, True)

    def test_parse_config_json_npm(self):
        data = {"npm": True}
        project_config = self.reader.parse_config_json("test", data)
        self.assertEqual(project_config.npm, True)

    def test_parse_config_json_trends(self):
        data = {"trends": "test"}
        project_config = self.reader.parse_config_json("test", data)
        self.assertEqual(project_config.history_path, "test")

    def test_parse_config_json_code_smells_default(self):
        data = {}
        project_config = self.reader.parse_config_json("test", data)
        self.assertEqual(
            project_config.code_smells.to_dict(), CodeSmellConfig().to_dict()
        )

    def test_parse_config_json_code_smells_disable_one(self):
        data = {"code_smells": {"camel_case_violation_function": False}}
        project_config = self.reader.parse_config_json("test", data)
        config = CodeSmellConfig()
        config.set("camel_case_violation_function", False)
        self.assertEqual(project_config.code_smells.to_dict(), config.to_dict())

    def test_parse_config_json_code_smells_disable_all(self):
        data = {"code_smells": False}
        project_config = self.reader.parse_config_json("test", data)
        config = CodeSmellConfig()
        config.disable_all()
        self.assertEqual(project_config.code_smells.to_dict(), config.to_dict())

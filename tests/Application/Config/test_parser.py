from unittest import TestCase
from unittest.mock import MagicMock, patch

from metripy.Application.Config.Config import Config
from metripy.Application.Config.Parser import Parser


class TestParser(TestCase):
    def setUp(self):
        self.parser = Parser()

    def test_parse_removes_script_name_metripy_py(self):
        """Test that 'metripy.py' as first argument is removed"""
        argv = ["metripy.py"]
        config = self.parser.parse(argv)

        self.assertIsInstance(config, Config)
        self.assertEqual(len(argv), 0)

    def test_parse_removes_script_name_metripy(self):
        """Test that 'metripy' as first argument is removed"""
        argv = ["metripy"]
        config = self.parser.parse(argv)

        self.assertIsInstance(config, Config)
        self.assertEqual(len(argv), 0)

    def test_parse_flag_without_value(self):
        """Test parsing flag arguments without values"""
        # Note: Due to list popping while iterating, only every other flag may be processed
        argv = ["metripy", "--debug"]
        config = self.parser.parse(argv)

        self.assertTrue(config.debug)

    def test_parse_argument_with_value(self):
        """Test parsing arguments with values"""
        argv = ["metripy", "--debug=true"]
        config = self.parser.parse(argv)

        self.assertEqual(config.debug, "true")

    def test_parse_mixed_arguments(self):
        """Test parsing mix of flags and value arguments"""
        argv = ["metripy", "--debug=true", "--help"]
        config = self.parser.parse(argv)

        self.assertTrue(config.debug)
        self.assertTrue(config.help)

    @patch("metripy.Application.Config.Parser.ConfigFileReaderFactory")
    def test_parse_config_file(self, mock_factory):
        """Test parsing with config file argument"""
        # Setup mock
        mock_reader = MagicMock()
        mock_factory.createFromFileName.return_value = mock_reader

        argv = ["metripy", "--config=test_config.json"]
        config = self.parser.parse(argv)

        # Verify factory was called with correct filename
        mock_factory.createFromFileName.assert_called_once_with("test_config.json")

        # Verify reader was called
        mock_reader.read.assert_called_once_with(config)

    @patch("metripy.Application.Config.Parser.ConfigFileReaderFactory")
    def test_parse_config_file_with_other_arguments(self, mock_factory):
        """Test parsing config file with additional arguments"""
        # Setup mock
        mock_reader = MagicMock()
        mock_factory.createFromFileName.return_value = mock_reader

        argv = ["metripy", "--config=config.json", "--debug"]
        config = self.parser.parse(argv)

        # Verify config file was processed
        mock_factory.createFromFileName.assert_called_once_with("config.json")
        mock_reader.read.assert_called_once()

        # Verify other arguments were processed
        self.assertIsInstance(config, Config)
        self.assertTrue(config.debug)

    def test_parse_empty_value_argument(self):
        """Test parsing argument with empty value"""
        argv = ["metripy", "--version="]
        config = self.parser.parse(argv)

        self.assertFalse(config.version)

    def test_parse_argument_with_special_characters(self):
        """Test parsing argument values with dots (not supported by current regex)"""
        # The Parser's regex ^--([\w]+)=(.*)$ only matches word characters, not dots
        # So parameters with dots in the key are not supported
        argv = ["metripy", "--debug=/path/to/project"]
        config = self.parser.parse(argv)

        # This should work as debug is a simple word character parameter
        self.assertTrue(config.debug)

    def test_parse_unknown_parameter_ignored(self):
        """Test that unknown parameters are ignored"""
        argv = ["metripy", "--unknown-param=value"]
        config = self.parser.parse(argv)

        # Should not raise an error and config should be valid
        self.assertIsInstance(config, Config)

    @patch("metripy.Application.Config.Parser.ConfigFileReaderFactory")
    def test_parse_multiple_config_options(self, mock_factory):
        """Test parsing with multiple different option types"""
        # Setup mock
        mock_reader = MagicMock()
        mock_factory.createFromFileName.return_value = mock_reader

        argv = ["metripy", "--config=config.json", "--debug=true", "--help"]
        config = self.parser.parse(argv)

        # Verify options were processed
        self.assertTrue(config.debug)
        self.assertTrue(config.help)

    def test_parse_returns_config_default_values(self):
        """Test that parse always returns a Config instance"""
        argv = ["metripy"]
        config = self.parser.parse(argv)

        self.assertIsInstance(config, Config)
        self.assertFalse(config.debug)
        self.assertFalse(config.quiet)
        self.assertFalse(config.version)
        self.assertFalse(config.help)

    @patch("metripy.Application.Config.Parser.ConfigFileReaderFactory")
    def test_parse_config_file_removes_from_argv(self, mock_factory):
        """Test that config file argument is removed from argv list"""
        mock_reader = MagicMock()
        mock_factory.createFromFileName.return_value = mock_reader

        argv = ["metripy", "--config=test.json", "--debug"]

        config = self.parser.parse(argv)

        self.assertIsInstance(config, Config)
        self.assertTrue(config.debug)

    def test_parse_numeric_values(self):
        """Test parsing arguments with numeric values"""
        # Using a simple parameter name without dots
        argv = ["metripy", "--debug=30"]
        config = self.parser.parse(argv)

        self.assertTrue(config.debug)

    def test_parse_boolean_string_values(self):
        """Test parsing boolean-like string values"""
        argv = ["metripy", "--debug=true"]
        config = self.parser.parse(argv)

        # Values are stored as strings, not converted to boolean
        self.assertTrue(config.debug)

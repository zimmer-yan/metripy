from unittest import TestCase
from metripy.Application.Config.File.PathResolver import PathResolver
from datetime import datetime

class TestPathResolver(TestCase):
    def setUp(self):
        self.path_resolver = PathResolver

    def test_resolve_date_iso_8601(self):
        path = self.path_resolver.resolve("test/{DATE_ISO_8601}")
        date = datetime.now().strftime("%Y-%m-%d")
        self.assertEqual(path, f"test/{date}")

    def test_resolve_date_year(self):
        path = self.path_resolver.resolve("test/{DATE_YEAR}")
        date = datetime.now().strftime("%Y")
        self.assertEqual(path, f"test/{date}")

    def test_resolve_date_month(self):
        path = self.path_resolver.resolve("test/{DATE_MONTH}")
        date = datetime.now().strftime("%m")
        self.assertEqual(path, f"test/{date}")

    def test_resolve_date_day(self):
        path = self.path_resolver.resolve("test/{DATE_DAY}")
        date = datetime.now().strftime("%d")
        self.assertEqual(path, f"test/{date}")

    def test_resolve_date_hour(self):
        path = self.path_resolver.resolve("test/{DATE_HOUR}")
        date = datetime.now().strftime("%H")
        self.assertEqual(path, f"test/{date}")

    def test_resolve_date_minute(self):
        path = self.path_resolver.resolve("test/{DATE_MINUTE}")
        date = datetime.now().strftime("%M")
        self.assertEqual(path, f"test/{date}")

    def test_resolve_date_second(self):
        path = self.path_resolver.resolve("test/{DATE_SECOND}")
        date = datetime.now().strftime("%S")
        self.assertEqual(path, f"test/{date}")

    def test_resolve_date_mixed(self):
        path = self.path_resolver.resolve("test/{DATE_YEAR}-{DATE_MONTH}-{DATE_DAY}")
        date = datetime.now().strftime("%Y-%m-%d")
        self.assertEqual(path, f"test/{date}")

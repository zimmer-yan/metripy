import os
import shutil
import sys
from datetime import datetime
from pathlib import Path

from py_template_engine import TemplateEngine

from metripy.Application.Info import Info
from metripy.Metric.ProjectMetrics import ProjectMetrics


class ProjectIndexRenderer:
    """Renders an HTML index page listing all analyzed projects with their stats."""

    def __init__(self, output_path: str):
        """
        Initialize the ProjectIndexRenderer.

        Args:
            output_path: Full path to the output HTML file (e.g., './build/html-index/index.html')
        """
        self.output_path = output_path
        self.output_dir = os.path.dirname(output_path)
        self.template_dir = self._find_template_dir()

    def _find_template_dir(self) -> Path:
        """Find the templates directory, checking multiple possible locations"""
        # TODO: refactor with htmlreporter
        package_dir = Path(__file__).parent.parent.parent  # metripy package root

        # List of possible locations to check
        possible_locations = [
            # Development: templates at project root
            package_dir.parent / "templates" / "html_report",
            # Alternative: templates inside metripy package
            package_dir / "templates" / "html_report",
            # System install location
            Path(sys.prefix) / "share" / "metripy" / "templates" / "html_report",
            # Fallback to cwd (for development)
            Path.cwd() / "metripy" / "templates" / "html_report",
        ]

        for location in possible_locations:
            if location.exists():
                return location

        return possible_locations[0]

    def render(
        self,
        project_metrics_list: list[tuple[str, ProjectMetrics, str | None]],
    ) -> None:
        """
        Render the project index HTML page.

        Args:
            project_metrics_list: List of tuples containing (project_name, ProjectMetrics, html_report_path)
        """
        # Ensure output directory exists
        os.makedirs(self.output_dir, exist_ok=True)

        # Copy static assets
        self._copy_static_assets()

        # Prepare project data for template
        projects_data = []
        total_loc = 0
        total_files = 0
        all_cc = []
        all_mi = []
        all_cog = []
        all_lcom4 = []

        for project_name, metrics, html_report_path in project_metrics_list:
            total_metrics = metrics.total_code_metrics

            # Calculate relative path from index to project report
            if html_report_path:
                report_link = self._get_relative_path(html_report_path)
            else:
                report_link = None

            project_data = {
                "name": project_name,
                "report_link": report_link,
                "loc": total_metrics.loc,
                "num_files": total_metrics.num_files,
                "avg_cc": round(total_metrics.avgCcPerFunction, 2),
                "avg_mi": round(total_metrics.maintainabilityIndex, 2),
                "avg_cog": round(total_metrics.avg_cog_complexity_per_function, 2),
                "avg_loc_per_function": round(total_metrics.avgLocPerFunction, 2),
                "avg_lcom4": round(total_metrics.avg_lcom4_per_class, 2),
                "health_class": self._get_health_class(
                    total_metrics.maintainabilityIndex,
                    total_metrics.avgCcPerFunction,
                    total_metrics.avg_cog_complexity_per_function,
                    total_metrics.avg_lcom4_per_class,
                ),
            }
            projects_data.append(project_data)

            # Accumulate totals for aggregate stats
            total_loc += total_metrics.loc
            total_files += total_metrics.num_files
            all_cc.append(total_metrics.avgCcPerFunction)
            all_mi.append(total_metrics.maintainabilityIndex)
            all_cog.append(total_metrics.avg_cog_complexity_per_function)
            all_lcom4.append(total_metrics.avg_lcom4_per_class)

        # Calculate aggregate statistics
        num_projects = len(project_metrics_list)
        avg_cc = sum(all_cc) / len(all_cc) if all_cc else 0
        avg_mi = sum(all_mi) / len(all_mi) if all_mi else 0
        avg_cog = sum(all_cog) / len(all_cog) if all_cog else 0
        avg_lcom4 = sum(all_lcom4) / len(all_lcom4) if all_lcom4 else 0

        aggregate_stats = {
            "num_projects": num_projects,
            "total_loc": total_loc,
            "total_files": total_files,
            "avg_cc": round(avg_cc, 2),
            "avg_mi": round(avg_mi, 2),
            "avg_cog": round(avg_cog, 2),
            "overall_health_class": self._get_health_class(
                avg_mi, avg_cc, avg_cog, avg_lcom4
            ),
        }

        # Render template
        template_data = {
            "projects": projects_data,
            "aggregate_stats": aggregate_stats,
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "version": Info().get_version(),
        }

        self._render_template("project_index.html", template_data)

    def _get_relative_path(self, html_report_path: str) -> str:
        """Calculate relative path from index to project report."""
        index_dir = os.path.dirname(os.path.abspath(self.output_path))
        report_index = os.path.join(os.path.abspath(html_report_path), "index.html")
        return os.path.relpath(report_index, index_dir)

    def _get_health_class(
        self,
        maintainability_index: float,
        avg_cc: float,
        avg_cog: float,
        avg_lcom4: float,
    ) -> str:
        """
        Get CSS class based on multiple code quality metrics.

        Calculates a composite health score using weighted metrics:
        - Maintainability Index (40%): higher is better (0-100 scale)
        - Cyclomatic Complexity (25%): lower is better
        - Cognitive Complexity (25%): lower is better
        - LCOM4 (10%): 1 is ideal, 0 or >1 is worse
        """
        # Normalize MI (already 0-100, higher is better)
        mi_score = min(max(maintainability_index, 0), 100)

        # Normalize CC (lower is better: 1-4=100, 5-10=75, 11-20=50, 21-40=25, 40+=0)
        if avg_cc <= 4:
            cc_score = 100
        elif avg_cc <= 10:
            cc_score = 100 - ((avg_cc - 4) / 6) * 25  # 100 -> 75
        elif avg_cc <= 20:
            cc_score = 75 - ((avg_cc - 10) / 10) * 25  # 75 -> 50
        elif avg_cc <= 40:
            cc_score = 50 - ((avg_cc - 20) / 20) * 50  # 50 -> 0
        else:
            cc_score = 0

        # Normalize Cognitive Complexity (similar thresholds to CC)
        if avg_cog <= 5:
            cog_score = 100
        elif avg_cog <= 10:
            cog_score = 100 - ((avg_cog - 5) / 5) * 25  # 100 -> 75
        elif avg_cog <= 20:
            cog_score = 75 - ((avg_cog - 10) / 10) * 25  # 75 -> 50
        elif avg_cog <= 40:
            cog_score = 50 - ((avg_cog - 20) / 20) * 50  # 50 -> 0
        else:
            cog_score = 0

        # Normalize LCOM4 (1 is ideal=100, 0 is bad=50, >1 progressively worse)
        if avg_lcom4 == 1:
            lcom4_score = 100
        elif avg_lcom4 == 0:
            lcom4_score = 50  # No methods in class is not great
        elif avg_lcom4 <= 2:
            lcom4_score = 100 - (avg_lcom4 - 1) * 50  # 1->100, 2->50
        elif avg_lcom4 <= 5:
            lcom4_score = 50 - ((avg_lcom4 - 2) / 3) * 50  # 2->50, 5->0
        else:
            lcom4_score = 0

        # Calculate weighted composite score
        composite_score = (
            mi_score * 0.30 + cc_score * 0.30 + cog_score * 0.30 + lcom4_score * 0.10
        )

        # Map composite score to health class
        if composite_score >= 80:
            return "excellent"
        elif composite_score >= 60:
            return "good"
        elif composite_score >= 40:
            return "fair"
        else:
            return "poor"

    def _copy_static_assets(self) -> None:
        """Copy CSS and other static assets to output directory."""
        # Create subdirectories
        css_dir = os.path.join(self.output_dir, "css")
        images_dir = os.path.join(self.output_dir, "images")

        os.makedirs(css_dir, exist_ok=True)
        os.makedirs(images_dir, exist_ok=True)

        # Copy styles.css for base styles
        src_css = os.path.join(self.template_dir, "css", "styles.css")
        if os.path.exists(src_css):
            shutil.copy(src_css, css_dir)

        # Copy logo
        src_logo = os.path.join(self.template_dir, "images", "logo.svg")
        if os.path.exists(src_logo):
            shutil.copy(src_logo, images_dir)

    @staticmethod
    def _stringify_values(obj):
        if isinstance(obj, dict):
            return {
                key: ProjectIndexRenderer._stringify_values(value)
                for key, value in obj.items()
            }
        elif isinstance(obj, list):
            return [ProjectIndexRenderer._stringify_values(item) for item in obj]
        else:
            return str(obj)

    def _render_template(self, template_name: str, data: dict) -> None:
        """Render a template with the given data."""
        data = self._stringify_values(data)
        template_path = os.path.join(self.template_dir, template_name)
        engine = TemplateEngine(template_path)
        content = engine.render(**data)

        with open(self.output_path, "w") as file:
            file.write(content)

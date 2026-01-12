---
layout: default
title: Home
---

# Metripy

<div style="text-align: center; margin: 2em 0;">
  <img src="logo.png" alt="Metripy Logo" width="120" height="120" style="margin-bottom: 1em;">
  <p style="font-size: 1.3em; color: #586069;">A multi-language, multi-project code metrics analysis tool</p>
</div>

## Overview

Metripy is a powerful static analysis tool that helps you understand your codebase's health, track technical debt, and monitor code quality trends over time. It supports multiple programming languages and provides comprehensive reports with beautiful visualizations.

## Key Features

🔍 **Multi-Language Support**
- Python (with radon)
- PHP (experimental)
- TypeScript (experimental)

📊 **Comprehensive Analysis**
- Cyclomatic complexity
- Maintainability index
- Halstead metrics
- Lines of code (LOC)
- Git history analysis
- Dependency analysis

📈 **Trend Tracking**
- Track code quality evolution over time
- Identify files that improved or degraded
- Monitor health distribution changes

🎨 **Beautiful Reports**
- Interactive HTML dashboards
- Color-coded metrics
- File tree with health indicators
- Git analysis visualization
- Dependency insights

## Quick Start

```bash
# Install metripy
pip install metripy

# Create a config file
cat > metripy.json << EOF
{
    "configs": {
        "my-project": {
            "base_path": "./",
            "includes": ["src/"],
            "extensions": ["py"],
            "git": {"branch": "main"},
            "reports": {
                "html": "./build/report"
            }
        }
    }
}
EOF

# Run analysis
metripy --config=metripy.json
```

## Why Metripy?

- **Multi-Project Support**: Analyze multiple projects in a single run
- **Language Agnostic**: Support for multiple programming languages
- **Rich Visualizations**: Understand your code at a glance
- **Trend Analysis**: See how your codebase evolves over time
- **Actionable Insights**: Identify files that need attention
- **Easy to Use**: Simple configuration and intuitive reports

## Get Started

<div style="display: flex; gap: 1em; margin: 2em 0;">
  <a href="installation" style="background: #3b82f6; color: white; padding: 0.8em 1.5em; border-radius: 6px; text-decoration: none; font-weight: bold;">Install Now</a>
  <a href="getting-started" style="background: #6b7280; color: white; padding: 0.8em 1.5em; border-radius: 6px; text-decoration: none; font-weight: bold;">Quick Guide</a>
  <a href="configuration" style="border: 2px solid #3b82f6; color: #3b82f6; padding: 0.8em 1.5em; border-radius: 6px; text-decoration: none; font-weight: bold;">Configuration</a>
</div>

## Example Report

Metripy generates beautiful, interactive HTML reports that include:

- **Dashboard Overview**: High-level metrics and trends
- **File Explorer**: Navigate your codebase with health indicators
- **Git Analysis**: Contributor insights and code hotspots
- **Dependency View**: Package versions and license distribution
- **Trends Page**: Track improvements and regressions over time

## Community & Support

- **GitHub**: [zimmer-yan/metripy](https://github.com/zimmer-yan/metripy)
- **Issues**: [Report bugs or request features](https://github.com/zimmer-yan/metripy/issues)
- **License**: MIT

---

<div style="text-align: center; color: #6b7280; margin-top: 3em;">
  Made with ❤️ by developers, for developers
</div>


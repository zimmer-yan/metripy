---
layout: default
title: Getting Started
---

# Getting Started

This guide will help you run your first code analysis with Metripy.

## Step 1: Install Metripy

```bash
pip install metripy
```

Verify installation:

```bash
metripy --version
```

## Step 2: Create a Configuration File

In your project root, create `metripy.json`:

### For Python Projects

```json
{
    "configs": {
        "my-project": {
            "base_path": "./",
            "includes": ["src/"],
            "excludes": ["__pycache__", ".venv", "tests/"],
            "extensions": ["py"],
            "pip": true,
            "git": {
                "branch": "main"
            },
            "reports": {
                "html": "./build/report"
            },
            "trends": "./build/historical/metrics.json"
        }
    }
}
```

### For TypeScript Projects

```json
{
    "configs": {
        "my-project": {
            "base_path": "./",
            "includes": ["src/"],
            "excludes": ["node_modules", "dist/", "*.test.ts"],
            "extensions": ["ts", "tsx"],
            "npm": true,
            "git": {
                "branch": "main"
            },
            "reports": {
                "html": "./build/report"
            }
        }
    }
}
```

### For PHP Projects

```json
{
    "configs": {
        "my-project": {
            "base_path": "./",
            "includes": ["src/"],
            "excludes": ["vendor/", "tests/"],
            "extensions": ["php"],
            "composer": true,
            "git": {
                "branch": "main"
            },
            "reports": {
                "html": "./build/report"
            }
        }
    }
}
```

## Step 3: Run Analysis

```bash
metripy --config=metripy.json
```

You should see output like:

```
Analying Project metripy...
Analyzing git history...
Git history analyzed
Analyzing code...
... 100% ...
Code analyzed
Analyzing pip packages...
Pip packages analyzed
Analyzing trends...
Importing data from ./build/historical-json-report/metripy.json...
Data imported successfuly
Trends analyzed
Done analying Project metripy
Generating reports for metripy...
Generating HTML report...
Rendering index page
Done rendering index page
Rendering files page
Files page generated successfully
Rendering git analysis page
Git analysis page generated successfully
Rendering dependencies page
Dependencies page generated successfully
Rendering top offenders page
Top offenders page generated successfully
Rendering trends page
HTML report generated in ./build/report/metripy directory
Create json report in ./build/json-report/metripy.json
Create git json report in ./build/json-report/metripy-git.json
Reports generated for metripy
```

## Step 4: View the Report

Open the HTML report in your browser:

```bash
# macOS
open ./build/report/index.html

# Linux
xdg-open ./build/report/index.html

# Windows
start ./build/report/index.html
```

## Understanding the Report

### Dashboard (index.html)

The main overview shows:
- **Total LOC**: All lines of code analyzed
- **Average Complexity**: Mean cyclomatic complexity
- **Maintainability Index**: Overall code maintainability (0-100)
- **Average Method Size**: Lines per function
- **Trend Badges**: Changes from previous analysis (if available)

Color coding:
- 🟢 **Green**: Good
- 🟡 **Yellow**: OK
- 🟠 **Orange**: Warning
- 🔴 **Red**: Critical

### Files Page

Browse your codebase with:
- **File Tree**: Hierarchical view with health indicators
- **Health Filters**: Show only files that need attention
- **File Details**: Click any file to see detailed metrics
- **Class/Function Breakdown**: Complexity of each component

### Git Analysis Page (if enabled)

Insights from your Git history:
- **Contributors**: Who's working on the code
- **Commit Timeline**: Activity over time
- **Code Hotspots**: Files that change frequently
- **Knowledge Distribution**: Team expertise mapping

### Dependencies Page (if enabled)

View your project dependencies:
- **Package Status**: Latest vs. required versions
- **License Distribution**: Legal compliance overview
- **GitHub Metrics**: Stars and download counts
- **Outdated Packages**: Packages needing updates

### Trends Page (if enabled)

Track changes over time:
- **Health Distribution Evolution**: How files move between health categories
- **Top Improved Files**: Complexity and maintainability wins
- **Files Needing Attention**: New problem areas

## Step 5: Track Trends (Optional)

To enable trend tracking, add a `trends` path to your config, this is the json output file from your past run:

```json
{
    "configs": {
        "my-project": {
            // ... other settings ...
            "trends": "./build/historical/metrics.json"
        }
    }
}
```

Run analysis regularly:

```bash
# Run daily, weekly, or after significant changes
metripy --config=metripy.json
```

Metripy will:
1. Load previous metrics from the trends file
2. Compare with current analysis
3. Show trend indicators and deltas
4. Update the trends file

## Common Workflows

### Quick Check

Just want a quick overview without Git or dependencies:

```json
{
    "configs": {
        "quick": {
            "base_path": "./",
            "includes": ["src/"],
            "extensions": ["py"],
            "reports": {
                "html": "./build/report"
            }
        }
    }
}
```

### Git Only

Only interested in Git metrics:

```json
{
    "configs": {
        "git-stats": {
            "base_path": "./",
            "git": {"branch": "main"},
            "reports": {
                "json-git": "./build/git-metrics.json"
            }
        }
    }
}
```

## Next Steps

Now that you're up and running:

- 📖 [Deep dive into Configuration](configuration) - Learn all config options
- 🎯 [Explore Features](features) - Understand all analysis capabilities
- 🔧 Advanced usage - Multi-project setups, custom workflows
- 📊 Integrate with your tools - CI/CD, dashboards, notifications

## Need Help?

- 📚 [Full Documentation](index)
- 🐛 [Report Issues](https://github.com/zimmer-yan/metripy/issues)
- 💬 [Discussions](https://github.com/zimmer-yan/metripy/discussions)

---

Happy analyzing! 🎉


---
layout: default
title: Configuration
---

# Configuration

Metripy uses JSON configuration files to specify analysis settings. You can configure multiple projects in a single file.

## Quick Configuration

Create a minimal `metripy.json` file:

```json
{
    "configs": {
        "my-project": {
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

Run with:

```bash
metripy --config=metripy.json
```

## Configuration Structure

### Root Object

```json
{
    "configs": {
        "project-name-1": { /* project config */ },
        "project-name-2": { /* project config */ }
    }
}
```

The `configs` object contains named project configurations. Each key is a project name.

## Project Configuration

### Basic Settings

#### `base_path` (required)
Base directory to analyze.

```json
"base_path": "./"
```

Can be relative to the config file or absolute:

```json
"base_path": "/absolute/path/to/project"
```

#### `includes` (optional)
Array of paths to include, relative to `base_path`.

```json
"includes": [
    "src/",
    "lib/"
]
```

If not specified, all files matching `extensions` are included.

#### `excludes` (optional)
Array of patterns to exclude.

```json
"excludes": [
    "__pycache__",
    "node_modules",
    "*.test.py",
    "build/",
    ".venv"
]
```

#### `extensions` (required)
Array of file extensions to analyze (without dots).

```json
"extensions": ["py"]
```

Multiple extensions:

```json
"extensions": ["py", "pyw"]
```

### Git Analysis

Enable Git history analysis:

```json
"git": {
    "branch": "main"
}
```

Options:
- `branch`: Git branch to analyze (default: `main`)

To disable git analysis, omit the `git` key.

### Dependency Analysis

#### Python (pip)

Analyzes `requirements.txt` or `pyproject.toml`:

```json
"pip": true
```

#### JavaScript/TypeScript (npm)

Analyzes `package.json`:

```json
"npm": true
```

#### PHP (Composer)

Analyzes `composer.json`:

```json
"composer": true
```

### Reports

Configure output formats and locations.

#### HTML Report

```json
"reports": {
    "html": "./build/report/my-project"
}
```

Generates an interactive HTML dashboard at the specified path.

#### JSON Report

```json
"reports": {
    "json": "./build/json-report/my-project.json"
}
```

Exports full analysis results as JSON.

#### Git JSON Report

```json
"reports": {
    "json-git": "./build/json-report/my-project-git.json"
}
```

Exports only git analysis as JSON.

#### Multiple Reports

```json
"reports": {
    "html": "./build/report/my-project",
    "json": "./build/json-report/my-project.json",
    "json-git": "./build/json-report/my-project-git.json"
}
```

### Trend Tracking

Enable historical tracking to see trends over time:

```json
"trends": "./build/historical-json-report/my-project.json"
```

Metripy will:
1. Read previous analysis from this file
2. Compare with current analysis
3. Calculate deltas and trends

## Complete Example

```json
{
    "configs": {
        "metripy": {
            "base_path": "./",
            "includes": [
                "metripy/"
            ],
            "excludes": [
                "__pycache__",
                "*.pyc",
                ".git",
                ".venv",
                "build/"
            ],
            "extensions": [
                "py"
            ],
            "pip": true,
            "git": {
                "branch": "main"
            },
            "reports": {
                "html": "./build/report/metripy",
                "json": "./build/json-report/metripy.json",
                "json-git": "./build/json-report/metripy-git.json"
            },
            "trends": "./build/historical-json-report/metripy.json"
        }
    }
}
```

## Multi-Project Configuration

Analyze multiple projects in one run:

```json
{
    "configs": {
        "backend": {
            "base_path": "./backend",
            "includes": ["src/"],
            "extensions": ["py"],
            "pip": true,
            "git": {"branch": "main"},
            "reports": {
                "html": "./build/report/backend"
            }
        },
        "frontend": {
            "base_path": "./frontend",
            "includes": ["src/"],
            "extensions": ["ts", "tsx"],
            "npm": true,
            "git": {"branch": "main"},
            "reports": {
                "html": "./build/report/frontend"
            }
        },
        "shared-library": {
            "base_path": "./shared",
            "includes": ["lib/"],
            "extensions": ["py"],
            "reports": {
                "html": "./build/report/shared"
            }
        }
    }
}
```

## Git-Only Configuration

Analyze only Git history (no code metrics):

```json
{
    "configs": {
        "project-git": {
            "base_path": "./",
            "git": {
                "branch": "main"
            },
            "reports": {
                "json-git": "./build/json-report/project-git.json"
            }
        }
    }
}
```

## Command-Line Arguments

### Config File

```bash
metripy --config=path/to/config.json
```

### Inline Arguments

You can override config file settings via command line, or omit a config file and define the full config via only arguments:

```bash
# Set project-specific values
metripy --configs.myproject.base_path="./src" --configs.myproject.extensions="py"

# Set boolean flags
metripy --quiet     # Suppress output
metripy --debug     # Enable debug logging
metripy --version   # Show version
metripy --help      # Show help
```

**Note**: Use dot notation for nested properties:

```bash
--configs.PROJECT_NAME.PROPERTY=VALUE
--configs.PROJECT_NAME.git="develop"
--configs.PROJECT_NAME.reports.html="./output"
--configs.PROJECT_NAME.trends="./path_to_old_config.json"
```

The config file contains has pip anaylsis enabled, but for your run you wish to disable it, use:
```bash
--configs.PROJECT_NAME.pip=false
```
It does not have pip analysis enabled, but for your run you wish to enable it:
```bash
--configs.PROJECT_NAME.pip
--configs.PROJECT_NAME.pip=true
```

To add a value to the list properties (includes, excludes, extension) just use PROPERTY=VALUE:
```bash
--configs.PROJECT_NAME.includes="some directory"
```

To empty a list property just use PROPERTY="". Afterwards you can add new values with the above:
```bash
--configs.PROJECT_NAME.includes=""
```


### Global Flags

| Flag | Description |
|------|-------------|
| `--quiet` | Suppress non-error output |
| `--debug` | Enable debug logging |
| `--version` | Display version and exit |
| `--help` | Show help message and exit |

## Best Practices

### 1. Exclude Test Files

If you don't want to analyze tests:

```json
"excludes": [
    "tests/",
    "test_*.py",
    "*_test.py"
]
```

### 2. Multiple Configs for Different Purposes

Create different config files for different use cases:

```bash
metripy.full.json      # Full analysis with Git and dependencies
metripy.quick.json     # Code metrics only
metripy.git.json       # Git analysis only
```

### 3. Use Relative Paths

Use relative paths for portability:

```json
"base_path": "./",
"reports": {
    "html": "./build/report"
}
```

### 4. Document Your Config

Add a README section explaining your config:

```markdown
## Running Code Metrics

```bash
metripy --config=metripy.json
```

Reports are generated in `./build/report/`
```

## Troubleshooting

### Config Not Found

Ensure the path to config file is correct:

```bash
# Use absolute path
metripy --config=/full/path/to/metripy.json

# Or relative to current directory
metripy --config=./config/metripy.json
```

### Invalid JSON

Validate your JSON using a linter:

```bash
# Online: jsonlint.com
# Or use Python
python -m json.tool metripy.json
```

### No Files Found

Check your `includes`, `excludes`, and `extensions`:

```json
"includes": ["src/"],        // Does this path exist?
"excludes": ["src/"],        // Are you excluding what you included?
"extensions": ["py"]         // Does this match your files?
```

### Git Branch Not Found

Ensure the specified branch exists:

```bash
git branch -a | grep main
```

Or use your default branch:

```json
"git": {
    "branch": "master"  // or "develop", etc.
}
```

---

[View Features →](features) | [Getting Started →](getting-started)


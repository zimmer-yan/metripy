---
layout: default
title: Installation
---

# Installation Guide

## Requirements

- **Python**: 3.11 or higher
- **Git**: Required for git analysis features
- **pip**: Python package manager

## Install from PyPI

The easiest way to install Metripy is via pip:

```bash
pip install metripy
```

### Verify Installation

```bash
metripy --version
```

You should see the version number (e.g., `0.2.8`).

## Install from Source

If you want to install the latest development version:

```bash
# Clone the repository
git clone https://github.com/zimmer-yan/metripy.git
cd metripy

# Install in development mode
pip install -e .
```

### Development Installation

For development work, install with dev dependencies:

```bash
pip install -e ".[dev]"
```

This includes testing and linting tools:
- pytest
- black (code formatter)
- flake8 (linter)
- mypy (type checker)
- isort (import sorter)

## Upgrade

To upgrade to the latest version:

```bash
pip install --upgrade metripy
```

## Dependencies

Metripy automatically installs the following dependencies:

### Core Dependencies
- **lizard** (1.18.0) - Multi-language code complexity analyzer
- **GitPython** (3.1.45) - Git repository analysis
- **radon** (6.0.1) - Python code metrics
- **requests** (2.32.5) - HTTP library for dependency data
- **py-template-engine** (≥0.1.0) - HTML report generation
- **packaging** (25.0) - Version parsing
- **toml** (0.10.2) - TOML file parsing
- **tree-sitter** (0.21.3) - Parser generator tool
- **tree-sitter-languages** (1.10.2) - Language parsers

## Platform Support

Metripy is tested and supported on:

- **macOS** (Intel & Apple Silicon)

### Python Version Issues

Check your Python version:

```bash
python --version
```

If you have multiple Python versions, use `python3.11` or `python3.12` explicitly:

```bash
python3.11 -m pip install metripy
```

### Git Not Found

Git analysis requires Git to be installed and in PATH:

```bash
# macOS
brew install git

# Ubuntu/Debian
sudo apt-get install git

# Fedora
sudo dnf install git
```

## Docker (Alternative)

If you prefer using Docker:

```bash
# Coming soon...
# docker pull metripy/metripy:latest
```

## Next Steps

- [Getting Started Guide](getting-started) - Run your first analysis
- [Configuration](configuration) - Learn about configuration options
- [Features](features) - Explore all features

## Uninstall

To uninstall Metripy:

```bash
pip uninstall metripy
```


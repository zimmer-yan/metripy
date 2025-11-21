# Metripy
A multilanguage, multi project code metrics analysis tool. 

[![PyPI version](https://img.shields.io/pypi/v/metripy.svg)](https://pypi.org/project/metripy/)
[![Tests](https://img.shields.io/badge/tests-138%20passed-brightgreen)](./tests)
[![Coverage](https://codecov.io/gh/zimmer-yan/metripy/branch/main/graph/badge.svg)](https://codecov.io/gh/zimmer-yan/metripy)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Downloads](https://img.shields.io/pypi/dm/metripy.svg)](https://pypi.org/project/metripy/)


# Languages
Supported languages
- Python
- Php
- Typescript (experimental)
- TBD

# Analysis types

## Code analysis
Analyses code with cyclomatic complexity, maintainability index, halstead metrics.

## Git analysis
Analyses git stats of the past months

## Dependeny analysis
Analyzses composer, npm or pip dependencies

More dependencies TBD

# Report formats

## Html
Generates an easy to read dashboard

TODO: as this application generates multi project reports, add central dashboard to have project specific insights at first glance

## Csv
Exports simple csv

## Json
Dumps full result into json

## Cli
Prints overview to cli, contains colorcoded tables and charts 

# Metrics

## Lines of code
The total number of lines in your source code, including comments and blank lines.

## Cyclomatic Complexity
A measure of the number of independent paths through your code.

## Cognitive Complexity
A measure of how difficult code is to understand based on its control flow and nesting.

## Maintainability Index
A composite metric that estimates how easy it is to maintain code, based on LOC, complexity, and comments.

## Average Method Size
The average number of lines per method or function in your codebase.

## Instability
A metric that measures how likely a module is to change based on its dependencies (ratio of efferent to afferent couplings).

## LCOM4
A metric that measures how well the methods of a class are related to each other. It checks if methods share common attributes, indicating cohesion.

# Configuration
Configuration is for the moment only possible with the `--config=<file>.json` option. More TBD

Sample configuraiton:
```json
{
    "configs": {
        "metripy": {
            "base_path": "./", // base path to look at
            "includes": [
                "metripy/" // paths to include from the base path on
            ],
            "excludes": [
                "__pycache__" // exclude patterns of paths / files
            ],
            "extensions": [
                "py" // file extensions to look at
            ],
            "git": { // if git is set, analyzes git history
                "branch": "main" // git branch to look at
            },
            "composer": true, // looks for base_path/composer.json and analyzes dependencies - for php projects
            "npm": true, // looks for base_path/package.json and analyzes dependencies - for ts/js projects
            "pip": true,
            // looks for base_path/requirements.txt or base_path/pyproject.toml and analyzes dependencies - for python projects
            "reports": {
                "html": "./build/report/metripy", // report should be put into this directory
                "json-git": "./build/json-report/metripy-git.json" // file where to put git json report
                // more types of reports TBA
            }
        },
        // next project name: { next config... } 
    }
}
```

## Configuration for only git stats
```json
{
    "configs": {
        "metripy-git": {
            "base_path": "./",
            "git": {
                "branch": "main"
            },
            "reports": {
                "json-git": "./build/json-report/metripy-git.json"
            }
        }
    }
}
```

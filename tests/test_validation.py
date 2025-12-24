import yaml
from pathlib import Path
from scripts import cli


def test_validate_example_project():
    project = yaml.safe_load(Path("examples/slavic_horror_short/project.yaml").read_text())
    schema = yaml.safe_load(Path("templates/project_schema.yaml").read_text())
    errors = cli.validate_config(project, schema)
    assert not errors


def test_validate_invalid_project():
    schema = yaml.safe_load(Path("templates/project_schema.yaml").read_text())
    project = {"title": "Bad Project"}  # missing required fields like pipeline_stages
    errors = cli.validate_config(project, schema)
    assert errors

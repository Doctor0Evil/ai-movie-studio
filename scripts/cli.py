#!/usr/bin/env python3
"""Simple CLI for validating and running ai-movie-studio project configs.

Commands:
  validate --project <path>
  run --project <path> [--stage <stage>|--stage full] [--dry-run]

This is intentionally lightweight and provides placeholder implementations for each
stage so example projects can be exercised in CI or locally without external models.
"""
import json
import os
import sys
from pathlib import Path

import click
import yaml

try:
    import jsonschema
except Exception:
    jsonschema = None

# Helpers
ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "templates" / "project_schema.yaml"


def load_yaml(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def validate_config(config: dict, schema: dict):
    if jsonschema is None:
        raise RuntimeError("jsonschema is required for validation (pip install jsonschema)")
    resolver = jsonschema.RefResolver(base_uri="", referrer=schema)
    validator = jsonschema.Draft7Validator(schema, resolver=resolver)
    errors = sorted(validator.iter_errors(config), key=lambda e: e.path)
    return errors


def write_sidecar(target: Path, info: dict):
    p = Path(target)
    sidecar = p.with_suffix(p.suffix + ".metadata.json")
    sidecar.write_text(json.dumps(info, indent=2), encoding="utf-8")
    return sidecar


def write_placeholder_png(path: Path):
    # Write a tiny 1x1 transparent PNG (binary). This avoids external deps like Pillow.
    png_bytes = bytes(
        [
            0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A, 0x00, 0x00, 0x00, 0x0D,
            0x49, 0x48, 0x44, 0x52, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x01,
            0x08, 0x06, 0x00, 0x00, 0x00, 0x1F, 0x15, 0xC4, 0x89, 0x00, 0x00, 0x00,
            0x0A, 0x49, 0x44, 0x41, 0x54, 0x78, 0x9C, 0x63, 0x00, 0x01, 0x00, 0x00,
            0x05, 0x00, 0x01, 0x0D, 0x0A, 0x2D, 0xB4, 0x00, 0x00, 0x00, 0x00, 0x49,
            0x45, 0x4E, 0x44, 0xAE, 0x42, 0x60, 0x82,
        ]
    )
    path.write_bytes(png_bytes)


# Stage implementations (placeholders)

def run_script_dev(project: dict, project_dir: Path, dry_run: bool = False):
    out = project_dir / "script.fountain"
    if dry_run:
        click.echo(f"[dry-run] would write {out}")
        return
    content = f"// Script for {project.get('title')}\n// Generated (placeholder)\n\\nINT. VILLAGE - NIGHT\nA low fog hangs over the fields.\n"
    out.write_text(content, encoding="utf-8")
    meta = {
        "artifact": str(out),
        "stage": "script_dev",
        "model": project.get("script_dev", {}).get("model", "<placeholder>"),
        "seed": project.get("script_dev", {}).get("deterministic_seed"),
    }
    write_sidecar(out, meta)
    click.echo(f"Wrote {out}")


def run_previs(project: dict, project_dir: Path, dry_run: bool = False):
    # Shotlist
    shotlist = project_dir / "shotlist.csv"
    storyboard_dir = project_dir / "storyboard" / "scene_01"
    animatic = project_dir / "animatic" / "scene_01.mp4"
    storyboard_dir.mkdir(parents=True, exist_ok=True)
    if dry_run:
        click.echo(f"[dry-run] would create {shotlist}, {storyboard_dir}/shot_01.png, {animatic}")
        return
    shotlist.write_text("scene,shot,description\n1,1,Establishing wide of village\n", encoding="utf-8")
    write_placeholder_png(storyboard_dir / "shot_01.png")
    (animatic).write_text("Placeholder animatic\n", encoding="utf-8")
    write_sidecar(shotlist, {"artifact": str(shotlist), "stage": "previs"})
    click.echo(f"Wrote {shotlist} and storyboard assets")


def run_visuals(project: dict, project_dir: Path, dry_run: bool = False):
    renders_dir = project_dir / "renders" / "scene_01"
    renders_dir.mkdir(parents=True, exist_ok=True)
    out = renders_dir / "shot_01.mp4"
    if dry_run:
        click.echo(f"[dry-run] would create {out}")
        return
    out.write_text("Placeholder render\n", encoding="utf-8")
    write_sidecar(out, {"artifact": str(out), "stage": "visuals"})
    click.echo(f"Wrote render {out}")


def run_audio(project: dict, project_dir: Path, dry_run: bool = False):
    voice_dir = project_dir / "audio" / "voice"
    voice_dir.mkdir(parents=True, exist_ok=True)
    out = voice_dir / "villager_elder.wav"
    if dry_run:
        click.echo(f"[dry-run] would create {out}")
        return
    out.write_text("Placeholder wav content\n", encoding="utf-8")
    write_sidecar(out, {"artifact": str(out), "stage": "audio"})
    click.echo(f"Wrote audio {out}")


def run_assemble(project: dict, project_dir: Path, dry_run: bool = False):
    manifest = project_dir / "assemble_manifest.json"
    if dry_run:
        click.echo(f"[dry-run] would create {manifest}")
        return
    # Collect artifact list
    artifacts = []
    for p in project_dir.rglob("*"):
        if p.is_file() and not p.name.endswith(".metadata.json"):
            artifacts.append(str(p))
    manifest.write_text(json.dumps({"artifacts": artifacts}, indent=2), encoding="utf-8")
    click.echo(f"Wrote manifest {manifest}")


@click.group()
def cli():
    """ai-movie-studio CLI"""
    pass


@cli.command()
@click.option("--project", "project_path", required=True, type=click.Path(exists=True))
def validate(project_path):
    """Validate a project.yaml against the schema."""
    project_path = Path(project_path)
    project = load_yaml(project_path)
    if not SCHEMA_PATH.exists():
        click.echo("Schema not found: templates/project_schema.yaml", err=True)
        sys.exit(2)
    schema = load_yaml(SCHEMA_PATH)
    try:
        errors = validate_config(project, schema)
    except RuntimeError as e:
        click.echo(str(e), err=True)
        sys.exit(2)
    if errors:
        click.echo("Validation failed:\n", err=True)
        for e in errors:
            click.echo(f"- {'.'.join([str(p) for p in e.path])}: {e.message}", err=True)
        sys.exit(1)
    click.echo("Validation passed ✅")


@cli.command()
@click.option("--project", "project_path", required=True, type=click.Path(exists=True))
@click.option("--stage", "stages", multiple=True, help="Stage to run; repeatable. Use 'full' to run pipeline_stages from config.")
@click.option("--dry-run", is_flag=True, default=False, help="Print actions without writing files.")
def run(project_path, stages, dry_run):
    """Run pipeline stage(s) for a project.yaml (creates placeholder artifacts).

Examples:
  scripts/cli.py run --project examples/slavic_horror_short/project.yaml --stage script_dev
  scripts/cli.py run --project examples/slavic_horror_short/project.yaml --stage full
"""
    project_path = Path(project_path)
    project = load_yaml(project_path)
    # Validate first
    schema = load_yaml(SCHEMA_PATH)
    try:
        errors = validate_config(project, schema)
    except RuntimeError as e:
        click.echo(str(e), err=True)
        sys.exit(2)
    if errors:
        click.echo("Project validation failed. Run `validate` for details.", err=True)
        for e in errors:
            click.echo(f"- {'.'.join([str(p) for p in e.path])}: {e.message}", err=True)
        sys.exit(1)
    # Determine stages
    if not stages or stages == ("full",):
        stages_to_run = project.get("pipeline_stages", [])
    else:
        if "full" in stages:
            stages_to_run = project.get("pipeline_stages", [])
        else:
            stages_to_run = list(stages)
    click.echo(f"Running stages: {stages_to_run}")
    project_dir = project_path.parent
    for s in stages_to_run:
        click.echo(f"--- {s} ---")
        if s == "script_dev":
            run_script_dev(project, project_dir, dry_run=dry_run)
        elif s == "previs":
            run_previs(project, project_dir, dry_run=dry_run)
        elif s == "visuals":
            run_visuals(project, project_dir, dry_run=dry_run)
        elif s == "audio":
            run_audio(project, project_dir, dry_run=dry_run)
        elif s == "assemble":
            run_assemble(project, project_dir, dry_run=dry_run)
        else:
            click.echo(f"Unknown stage: {s}", err=True)


if __name__ == "__main__":
    cli()

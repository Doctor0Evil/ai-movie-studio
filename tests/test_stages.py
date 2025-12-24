import yaml
from pathlib import Path
from scripts import cli


def test_run_script_dev_creates_script_and_metadata(tmp_path):
    proj = {
        "title": "Test",
        "genre": "Slavic Horror",
        "format": "short",
        "pipeline_stages": ["script_dev"],
        "script_dev": {"model": "m", "deterministic_seed": 1},
    }
    # run stage
    cli.run_script_dev(proj, tmp_path)
    script = tmp_path / "script.fountain"
    assert script.exists(), "script.fountain not created"
    meta = tmp_path / "script.fountain.metadata.json"
    assert meta.exists(), "metadata sidecar not created"


def test_run_previs_creates_shotlist_and_storyboard(tmp_path):
    proj = {
        "title": "Test",
        "genre": "Slavic Horror",
        "format": "short",
        "pipeline_stages": ["previs"],
    }
    cli.run_previs(proj, tmp_path)
    shotlist = tmp_path / "shotlist.csv"
    assert shotlist.exists(), "shotlist.csv not created"
    storyboard_img = tmp_path / "storyboard" / "scene_01" / "shot_01.png"
    assert storyboard_img.exists(), "storyboard image not created"


def test_run_assemble_collects_artifacts(tmp_path):
    # create some artifacts
    (tmp_path / "foo.txt").write_text("x")
    (tmp_path / "bar.png").write_text("x")
    cli.run_assemble({}, tmp_path)
    manifest = tmp_path / "assemble_manifest.json"
    assert manifest.exists()
    data = yaml.safe_load(manifest.read_text())
    assert "artifacts" in data

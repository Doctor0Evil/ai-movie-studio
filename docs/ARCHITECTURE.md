# ai-movie-studio — Architecture Overview 🗺️

Purpose
-------
This document describes the high-level architecture, responsibilities, data artifacts, and integration patterns for `ai-movie-studio`. It is intended for contributors, integrators, and studio engineers who will implement, extend, or plug into the pipelines.

Goals
-----
- Make the repo easy to audit and extend by clearly separating stages (script_dev, previs, visuals, audio).  
- Define artifact formats and contracts so pieces can be run independently or chained.  
- Provide adapter/CLI patterns for third‑party models and services.  
- Capture operational, provenance, and safety requirements (model attribution, content warnings).

High-level diagram
------------------
Flow (simplified):

Idea -> Script Dev -> Previs -> Visuals -> Audio -> Assemble -> Publish

ASCII view:

  [Idea/Prompt] 
       |
       v
  [script_dev]
       |
       v
  [previs]
  (shotlists, storyboards, animatics)
       |
       v
  [visuals] <-> [tools/video_generation_adapter]
       |
       v
  [audio]  <-> [tools/audio_stack_adapter]
       |
       v
  [assemble] (stems, renders, metadata) -> examples/ + REPORT.md

Components & responsibilities
----------------------------
- pipeline/script_dev/
  - Purpose: Convert concept → loglines → outlines → script (Fountain/FDX).  
  - Artifacts: `project.yaml`, `script.fountain`, `coverage/*.json`.
  - Contracts: `generate_outline(input: yaml) -> outline.yaml`.

- pipeline/previs/
  - Purpose: Scene break down, shot planner, image stubs, animatic assembly.  
  - Artifacts: `shotlist.csv`, `storyboard/scene_##/shot_##.png`, `animatic/scene_##.mp4`.
  - Contracts: `breakdown(script.fountain) -> scenes.yaml`; `plan_shots(scene) -> shotlist.csv`.

- pipeline/visuals/
  - Purpose: Render frames/video (2D, stylized video, virtual 3D).  
  - Artifacts: `scene_config.yaml`, `render_queue.json`, `renders/scene_##/shot_##.*`.
  - Contracts: `render_scene(scene_config) -> render_queue.json -> renders/`.

- audio/
  - Purpose: TTS, SFX, score generation, stems export.  
  - Artifacts: `voice/*.wav`, `sfx/*.wav`, `music/stems/*.wav`, `mix/*.rpp`.
  - Contracts: `tts(dialogue_spec) -> wav`; `compose(scene_description) -> stems/`.

- tools/ (adapters)
  - Purpose: Thin wrappers and documented contracts for models/services (video, TTS, multi-agent systems).  
  - Each adapter contains: `README.md`, `config.example.yaml`, `cli.py`.
  - Recommended interface: `Adapter.run(input: dict) -> ArtifactLocation` and idempotent, testable behavior.

Artifacts & provenance
----------------------
- All generated artifacts must include metadata in a `metadata.json` or YAML sidecar (artifact path + provenance):
  - model: name + version/commit
  - prompt: text or reference to `prompts/` file
  - seed and RNG settings
  - timestamp and author (human who approved/curated)
  - license / third-party attributions

Example sidecar (JSON):

```json
{
  "artifact": "storyboard/scene_01/shot_01.png",
  "model": "text-image-v1",
  "model_version": "v2.3.1",
  "prompt_ref": "prompts/genres/slavic_horror/scene_seed.md",
  "seed": 12345,
  "created_by": "cli/scripts/runner.py",
  "created_at": "2025-12-23T12:00:00Z",
  "license": "cc0",
  "notes": "Human color-grading applied by @editor"
}
```

Project config (`project.yaml`) schema (recommended)
---------------------------------------------------
```yaml
title: "Working Title"
genre: "Slavic Horror"
tone: "slow-burn"
format: "short|feature|episodic"
target_runtime_minutes: 12
lang: ["en", "uk"]
pipeline_stages:
  - script_dev
  - previs
  - visuals
  - audio
  - assemble
```

Reporting & example `REPORT.md`
-------------------------------
Each example project must include `REPORT.md` documenting:
- Which AI models were used (name + version).  
- Which steps were human-curated and why.  
- Time taken for each stage (estimate).  
- Safety or cultural review notes and content warnings.  

Adapter design guidelines
-------------------------
- Keep adapters thin and deterministic where possible.  
- Provide mocks and fixtures for CI.  
- Expose: `validate_config(config)`, `dry_run(input)`, `run(input)`.
- Use `config.example.yaml` and environment variables for secrets.

Testing & CI recommendations
----------------------------
- Unit tests for core logic (parsers, validators, transforms).  
- Integration tests that run in a mocked mode when credentials are missing.  
- Linting + formatting checks on PRs.  
- Add an examples smoke-test: run `scripts/cli.py run --project examples/slavic_horror_short/project.yaml --stage script_dev` in CI and mark as optional (short or smoke mode).

Operational concerns
--------------------
- Secrets: never commit. Use `.env` or CI secret stores.  
- Model keys: reference using names in `config` and store endpoints separately.  
- Resource planning: large model jobs should be queued and have retry/backoff.

Security & Responsible AI
-------------------------
- Human-in-the-loop approval gates for content that can be harmful.  
- Cultural review process for folklore and real-world cultural material (label: `culture-review`).  
- Maintain `MODELS.md` or `THIRD_PARTY.md` recording model licenses and dataset provenance.

Conventions & best practices
----------------------------
- Use YAML for configs and metadata, CSV for shotlists, and JSON for machine-checked reports.  
- Use stable file paths and semantic naming: `storyboard/scene_01/shot_01.png`.  
- Version prompts and prompt packs in `prompts/` with clear examples and expected output format.

Open questions & next steps
--------------------------
- Define a minimal `project.yaml` validation CLI and schema.  
- Create templates for `REPORT.md` and `metadata.json` sidecars.  
- Provide diagrams (SVG/PNG) for the README and docs pages.

---

This file should be a living document — please open an Issue or PR if you want to propose changes to the architecture or add implementation guidance.
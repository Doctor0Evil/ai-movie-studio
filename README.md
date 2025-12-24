# ai-movie-studio — AI Movie‑Production Reference Architecture 🎬🤖

[![Status: Draft](https://img.shields.io/badge/status-draft-yellow)](#)
[![License: Apache-2.0](https://img.shields.io/badge/license-Apache--2.0-blue)](#)
[![Build](https://img.shields.io/badge/build-ci--pipeline-pending)](#)
[![Coverage](https://img.shields.io/badge/coverage-tbd-lightgrey)](#)

A reference architecture and open-source starter kit for AI‑assisted film production — from idea to animatic, to AI‑generated visuals and audio. Designed for studios, tool builders, and indie creators, with a **specialization** in horror and Slavic‑horror that can be extended to any genre.[web:7][web:8]
​

Vision
Give studios, indie teams, and tool builders a modular blueprint for AI‑first production.
​

Let humans stay in charge creatively while AI handles repetitive craft: drafts, boards, animatics, rough cuts, and soundbeds.
​

---

## Table of Contents 📚

- [Why this repo?](#why-this-repo-)
- [Project overview](#project-overview-)
- [Repository layout](#repository-layout-)
- [Core pipelines](#core-pipelines-)
- [Specialization: Horror & Slavic-horror](#specialization-horror--slavic-horror-)
- [Prompt packs & co‑creation](#prompt-packs--co-creation-)
- [Tools & integrations](#tools--integrations-)
- [Quickstart](#quickstart-)
- [Security & Responsible AI](#security--responsible-ai-)
- [Contributing & Code of Conduct](#contributing--code-of-conduct-)
- [License & attribution](#license--attribution-)
- [References](#references-)

---

## Why this repo? 💡

`ai-movie-studio` aims to provide an industry‑ready, auditable pipeline for AI‑assisted production workflows, mapping closely to real film studio stages.[web:7][web:8] It focuses on making AI a creative amplifier rather than a replacement, keeping humans in the loop for direction, curation, and final approval.[web:7][web:11]

Key goals:

- Prototype end‑to-end AI‑generated shorts quickly (script → storyboard → animatic → visuals → audio).[web:7][web:8]  
- Offer reference integrations into emerging open-source film automation and video generation projects.[web:7][web:8]  
- Provide reusable patterns for genre‑specific customization, starting with horror and Slavic‑horror.  
​

## Repository layout 🗂️
This layout is **aspirational**; create only the folders you actually use and adjust as the project matures.

- `docs/` — architecture diagrams, stakeholder docs (e.g., `ARCHITECTURE.md`, `FOR_STUDIOS.md`, `HORROR_SPECIALIZATION.md`).  
- `prompts/` — curated prompt libraries, including `prompts/genres/slavic_horror/` for folklore‑driven horror.  
- `scripts/` — CLIs and helper scripts (e.g., `scripts/cli.py`) to run pipelines end‑to‑end.  
- `pipeline/` — core pipeline modules, e.g.:
  - `pipeline/script_dev/`
  - `pipeline/previs/`
  - `pipeline/visuals/`
- `audio/` — TTS, SFX, and music pipelines plus DAW template references.  
- `tools/` — adapters for external models/services (e.g., `filmagent_adapter/`, `video_generation_adapter/`).[web:7][web:8]  
- `templates/` — project YAML specs, scene configs, and CI templates.  
- `examples/` — runnable projects like `examples/slavic_horror_short/` with `REPORT.md` explaining human/AI roles.  

docs/ – architecture, studio/investor docs, horror specialization notes.
​

See the `Repository layout` section above for folder purposes.
​

See the `Repository layout` section above for folder purposes.
​

See the `Repository layout` section above for folder purposes.

See the `Repository layout` section above for folder purposes.
​

See the `Repository layout` section above for folder purposes.

See the `Repository layout` section above for folder purposes.
​

See the `Repository layout` section above for folder purposes.

See the `Repository layout` section above for folder purposes.

Core Pipelines
1. Idea → Script
Location: `pipeline/script_dev/`

Modules:

- `idea_to_logline/` — generate multiple logline variants per genre (Slavic‑horror, psychological horror, etc.).  
​

- `outline_generator/` — build scene‑by‑scene outlines and escalation curves.  

- `screenplay_builder/` — export to formats like Fountain or Final Draft XML based on templates.[web:10]  
​

- `coverage_tools/` — automated coverage reports (logline, synopsis, comps, risks).  
​

Example project spec: `templates/script_project.yaml` (title, genre, tone, constraints, target runtime).
### 2) Script → Storyboard → Shot list 🎞️
Location: `pipeline/previs/`

- `scene_breakdown/` — parse script into scenes, beats, characters, and horror motifs.  

- `shot_planner/` — propose camera setups, lenses, and movements per shot.  
​

- `image_stub_generator/` — generate grayscale keyframes or style studies via diffusion/video‑image models.[web:8]  
​

- `animatic_builder/` — assemble frames + temp audio into animatics (MP4).  
​

Typical outputs:

- `shotlist.csv`
- `storyboard/scene_##/shot_##.png`
- `animatic/scene_##.mp4`  

### 3) Visual generation 🎨
Location: `pipeline/visuals/`

Tracks:

- `animated_2d/` — keyframes → tweening → renders.  

- `stylized_video/` — text/shot‑conditioned video generation (Open‑Sora‑style).[web:8]  
​

- `3d_virtual_film/` — virtual camera + environment placement, inspired by multi‑agent virtual film systems.[web:7]  
​

Each scene may use:

- `scene_config.yaml` — model selection, prompts, seeds, style constraints.  
- `render_queue.json` — batch render plan for scenes/shots.  
### 4) Audio & music 🔊
Location: `audio/`

Sub‑pipelines:

- `voice/` — TTS and voice‑cloning configs for characters and narration.
  - Language and accent presets (including Eastern European voices).  

  Examples:
  ```
  audio/voice/
  ├── configs/
  │   ├── villager_elder.json
  │   ├── possessed_child.json
  │   └── narrator_calm_ukrainian.json
  └── tts_dialogue_pipeline.py
  ```
​

Language and accent presets (including Eastern European voices).

Examples:

text
audio/voice/
├── configs/
│   ├── villager_elder.json
│   ├── possessed_child.json
│   └── narrator_calm_ukrainian.json
└── tts_dialogue_pipeline.py
- `sfx/` — procedural or AI‑assisted SFX generation (winds, drones, creaks).
AI tools for atmospheres, drones, impacts; can batch‑render asset lists.
​

Organized libraries:

```
audio/libraries/
├── atmospheres/
│   ├── wind_forest_night.wav
│   ├── underground_drone_01.wav
├── impacts/
└── rituals/
```
- `music/` — AI composition templates and stems for DAW workflows.[web:9]
Prompt recipes for generating underscore, themes, and ritual motifs.

Notebooks and scripts exporting stems per instrument into DAWs.

Templates and notebooks for exporting stems into DAWs (e.g., Reaper, Ableton, Pro Tools).

Pipeline docs: `audio/docs/PIPELINE_AUDIO.md` walks through:

1. Generate AI dialogue.
2. Apply horror FX chains.
3. Layer atmospheres and drones.
4. Export stems for human mixing.

## Tools & integrations 🔌
Adapters in `tools/` provide thin, testable interfaces to external systems.[web:7][web:8]

Examples:

- `tools/filmagent_adapter/` — bridge to FilmAgent‑style multi‑agent virtual film workflows.[web:7]  
​

- `tools/hitchcock_adapter/` — experimental multi‑agent script→shot pipelines inspired by hackathon projects.[web:9]  
​

- `tools/video_generation_adapter/` — interface for Open‑Sora‑like video generators.[web:8]  
​

- `tools/audio_stack_adapter/` — script→voiceover/SFX/music orchestration.  
​

- `tools/scriptgen_adapter/` — optional integration with third‑party script tools.  
​

Each adapter should ship with:

- Its own `README.md`  
- Example config (e.g., `config.example.yaml`)  
- CLI entry point (e.g., `cli.py`)  

## Prompt packs & co‑creation 📝
Folder: prompts/

Suggested structure:

- `prompts/scripts/` — loglines, beats, scene prompts, character bios.  
- `prompts/genres/slavic_horror/` — specialized seeds like `slavic_horror_short/scene_seed.md`.  
- `prompts/assistants/` — role‑based agents (script doctor, editor, composer, producer).  

Example ready‑made pack:

- `prompts/genres/slavic_horror/slavic_horror_short/`  
  - `scene_seed.md`  
  - `visual_style.md`  
  - `sound_design.md`  
  - `safety_and_taboos.md`  

These packs should define: input expectations, output schema, and example completions for reproducibility.[web:6]
Example: prompts/genres/slavic_horror/scene_seed.md (already sketched in prior message) guides creation of quiet, dread‑heavy scenes.

Assistant prompts (prompts/assistants/):

script_doctor.md – improve and tighten human drafts.

editor_notes.md – AI gives pacing/structure feedback.

music_direction.md – AI suggests musical approach.

marketing_trailer_ideas.md – trailer beats, loglines, taglines.

These show how humans collaborate with AI, not get replaced by it.
​

## Example projects 🎞️
Folder: examples/

- `examples/slavic_horror_short/` — complete micro‑production with `project.yaml`, `script.fountain`, `shotlist.csv`, `storyboards/`, `renders/`, `audio_mix/`, and `REPORT.md` that documents timeline, tools used, and human touchpoints.

- `examples/ai_animated_trailer/` — a 30‑second AI‑heavy teaser demonstrating a high‑automation pipeline.

These reference builds are designed explicitly so major studios and investors can see concrete outputs and evaluate where to plug into their own pipelines.
​

## Documentation 📚
Folder: docs/

Recommended:

ARCHITECTURE.md – overall diagrams, module interactions.
​

FOR_STUDIOS.md – how to adopt pieces: dev coverage, animatics, dubbing, etc.

FOR_INVESTORS.md – cost‑saving areas, scalable content formats.

HORROR_SPECIALIZATION.md – why horror/Slavic‑horror is emphasized; best‑practice prompts, audio styling.

Contributions are welcome, especially from filmmakers, technologists, and researchers working on AI‑assisted production.

Suggested files:

- `CONTRIBUTING.md`
  - How to propose changes and open PRs.  
  - Coding standards, testing expectations, and documentation requirements.  
  - Guidelines for logging prompts, seeds, and human decision points in `REPORT.md`.  
- `CODE_OF_CONDUCT.md`
  - Expected behavior and anti‑harassment policies based on a standard template (e.g., Contributor Covenant).  

Contributor expectations:

- Prefer small, well‑scoped PRs.  
- Include/update `REPORT.md` for new `examples/` explaining human vs. AI contributions.  
- Add or update tests for any pipeline or adapter changes.  

## License & attribution 📜

**Suggested license:** Apache 2.0, to support wide reuse while providing explicit patent grants and contributor protections.[web:8]  

Action items:

- Add `LICENSE` with Apache‑2.0 text.  
- Add `THIRD_PARTY.md` to list:
  - External models and datasets.  
  - Libraries and tools (FilmAgent, Open‑Sora, etc.) with links and licenses.[web:7][web:8]  

Users remain responsible for complying with all third‑party licenses and local regulations when deploying or commercializing derivative works.

---

## References 🔗

Some related projects and resources that inspired this architecture:

- FilmAgent — multi‑agent virtual film automation in 3D spaces: https://github.com/HITsz-TMG/FilmAgent[web:7][web:11]  
- Open‑Sora — open video generation stack: https://github.com/hpcaitech/Open-Sora[web:8]  
- Hitchcock‑style multi‑agent storytelling: hackathon write‑up — https://elevenlabs-worldwide-hackathon.devpost.com/submissions/621602-lossfunk[web:9]  
- General guidance on crafting AI‑friendly READMEs — https://benhouston3d.com/blog/crafting-readmes-for-ai[web:6]  

# Contributing to ai-movie-studio 🤝

Thanks for your interest in contributing — whether as a filmmaker, developer, prompt author, or audio engineer. This document explains the preferred workflow, standards, and expectations so we can accept high-quality contributions quickly.

## ⚡ Quick start

- Fork the repo, create a branch from `main`, implement your change, and open a Pull Request (PR) targeting `main`.
- Branch naming: `feature/<short-description>`, `fix/<short-description>`, `docs/<short-description>`, `examples/<short-description>`.
- Keep PRs small and focused; they review faster.

## Where to begin

- File issues for bugs or feature requests. Use clear titles and include reproduction steps or example prompts/outputs when applicable.
- If you want to discuss larger design changes, open an Issue and tag it `proposal` or start a Discussion (if enabled).

## PR workflow

1. Create a branch for your change.  
2. Ensure changes pass linters and tests locally.  
3. Write a clear PR description with:
   - What you changed and why.
   - How to run/test locally (commands).  
   - For prompt/seed changes: include the prompt, model name/version, seed(s), and sample outputs (redact sensitive content).  
4. Add changelog or update `REPORT.md` for example projects when relevant.  
5. Link related issues and request specific reviewers if appropriate.

## PR checklist (maintainers may request these before merging)

- [ ] PR targets `main` branch (or other branch if specified).  
- [ ] CI passes (linting, tests).  
- [ ] New code has tests or documented rationale.  
- [ ] Documentation and examples updated (`README.md`, `docs/*`, `examples/*`).  
- [ ] For creative assets and prompts: include `REPORT.md` entry describing human interventions, model versions, seeds, and any safety considerations.  
- [ ] No secrets or credentials are included in the PR.

## Coding & style

- Use idiomatic code for the language in the edited files (Python/JS/TS recommended).  
- Run formatters and linters before PR (examples we recommend): `black`, `isort`, `flake8` for Python; `prettier`, `eslint` for JS/TS.  
- Add or update unit/integration tests for core logic (pipelines, adapters, utilities).

## Documentation

- Keep docs concise and practical: `README.md` for high-level, `docs/` for deep dives, `templates/` for configs.  
- When adding or changing prompts, add an example input and output, and document constraints and expected schema (prompts are treated as versioned assets).

## Data, prompts, and provenance

When submitting prompts, seeds, or model-driven examples, always include:
- Prompt text (or a well-documented summary).  
- Model name and version (or endpoint).  
- Seed(s) used and any non-deterministic settings.  
- Attribution for third‑party assets or data.  
- Any license or usage constraints.

This helps reproducibility and legal clarity for contributors and downstream users.

## Sensitive content & horror specialization

- This project contains a horror specialization; contributors must follow sensitivity guidelines included in `docs/HORROR_SPECIALIZATION.md`.  
- Avoid harmful stereotypes and exploitative depictions of cultures. When a contribution touches on folklore or cultural material, flag it for cultural review (`label: culture-review`).  
- Include content warnings in `REPORT.md` for any example that contains mature, graphic, or potentially distressing content.

## Security & secrets

- Never put API keys, credentials, or private data into the repository. Use placeholder variables in config examples and document how to securely provide secrets (e.g., environment variables, secrets manager).
- If you discover a security vulnerability, please report it privately to the maintainers: `security@your-org.example` (replace with real address) or open a private issue.

## Tests & CI

- New features must include tests where applicable.  
- If you add external adapters, include integration tests that can be skipped/mocked when credentials are absent.  

## Governance & licensing

- All contributions are under the repository license (suggested: Apache‑2.0).  
- By submitting a PR you agree to the repository's DCO/CLA policy (if enabled by maintainers).

## Getting help

- Tag maintainers in PRs for review or post in Discussions/Issues.  
- For process questions, open an issue labeled `meta`.

## Acknowledgements

Thanks for contributing — your work helps make `ai-movie-studio` a useful, responsible reference architecture for studios and creators.

---

*Note: Replace `security@your-org.example` with a real private reporting email before publishing.*
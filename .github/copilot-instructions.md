<!-- .github/copilot-instructions.md - guidance for AI coding agents -->
# Copilot / Agent Instructions (concise)

Purpose: Help an AI coding agent be productive in this repository immediately.

**Quick Setup**:
- **Activate venv (PowerShell):** `Set-Location -LiteralPath 'E:\GRIFFIN'` then `. .\.venv\Scripts\Activate.ps1`
- **Install deps:** `python -m pip install --upgrade pip` then `python -m pip install -r requirements.txt`
- **Format:** `python -m black .`
- **Run tests:** `python -m pytest -q`

**Big Picture / Architecture**:
- Primary dataflow: `core` → `domain` → `services` → `ace` → `cli` (see `README.md` and `ARCHITECTURE.md`).
- Project uses a hyper-modular, single-responsibility file pattern: one concept or ESI endpoint per file.
- ACE is the cognition/orchestration layer — key folders: `ace/core`, `ace/layers`, `ace/orchestrator`.

**Conventions & Patterns (discoverable)**:
- **Single-file-per-concept:** create one small module per value-object, entity, use-case, or connector file.
- **Domain purity:** files under `domain/` are pure logic (no IO). Put transports in `infra/` or `services/`.
- **Ports & Adapters:** define a `*_port.py` Protocol in `infra/` and the implementation in `*_impl.py`.
- **ESI endpoints:** one file per endpoint under `services/connectors/esi/...` and mapping functions under `services/mappers/esi_to_domain/...`.
- **Naming:** follow the pattern `get_<resource>.py`, `map_<resource>.py`, `sync_<resource>.py` when adding connectors, mappers, and sync tasks.

**Integration Points / External deps**:
- ESI OAuth: repo README documents the app callback `eveauth-griffin://callback/` — token handling should live under `infra/security`.
- SDE + ESI are fused in services and mapped into `domain/` objects via mappers.
- Key top-level files: `pyproject.toml`, `requirements.txt`, `README.md`, `ARCHITECTURE.md`.

**Where to add specific code**:
- New ESI connector: `services/connectors/esi/<resource>/get_<resource>.py`
- Mapper for that endpoint: `services/mappers/esi_to_domain/<resource>/map_<resource>.py`
- Repository/port: add a protocol in `infra/` (e.g., `character_repo_port.py`) and impl in `services/repositories/`.

**Testing / PR checklist (concrete)**:
- Keep PRs small and single-responsibility.
- Add unit tests for new domain logic under a mirrored test path.
- Run `python -m black .` before opening PR.
- Do not commit secrets — use `.env` or `infra/security/*` for credentials.

**Merging existing instruction files**:
- If a pre-existing `.github/copilot-instructions.md` exists, preserve its top-level sections (Purpose, Setup, Commands) and append or reconcile architecture/command sections below.

**Examples from repo**:
- See `README.md` for exact dev commands and the architecture summary.
- Example connector/mapping pattern: `services/connectors/esi/characters/get_character_info.py` → `services/mappers/esi_to_domain/characters/map_character_info.py`.
- ACE orchestrator entrypoints: `ace/orchestrator/orchestrator.py` and `ace/layers/*`.

If anything here is unclear or you want a different emphasis (more test detail, CI, or commit conventions), tell me which sections to expand or change.

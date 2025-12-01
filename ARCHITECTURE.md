# 📘 G.R.I.F.F.I.N. — Architecture & Roadmap

### Galactic Recon & Intel Framework for Fleet Insight & Navigation  
AI-enhanced EVE Online companion, intel engine, and multi-character orchestration system, built on a customized ACE cognitive architecture.

---

## 🧠 1. Overview

G.R.I.F.F.I.N. is an advanced, modular EVE Online application designed to function as:

- A shipboard AI copilot for a single pilot or entire stable of alts  
- A fleet-aware strategic intel engine  
- An account-wide economic & industrial brain  
- A multi-character orchestration layer for complex operations  
- A CLI-driven AGI-like presence (“Griffin”) built on the ACE Framework

It fuses ESI (live telemetry), SDE (static world data), ACE (6-layer cognitive stack), and local analytics + vector memory + hypergraph analysis into a hyper-modular Python 3.12 codebase located at `E:\GRIFFIN`.

---

## 🧬 2. Current Project State

- Root directory: `E:\GRIFFIN`  
- Python 3.12 (via `.venv`)  
- Dev tooling: `black`, `ruff`, `pytest`, `mypy`, `pip-tools`  
- EVE Dev App: `G.R.I.F.F.I.N.` with callback `eveauth-griffin://callback/` and broad ESI scopes

---

## 🧱 3. Developer Quickstart

PowerShell
```powershell
Set-Location -LiteralPath 'E:\GRIFFIN'
. .\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

cmd.exe
```bat
cd /d E:\GRIFFIN
.\.venv\Scripts\activate.bat
```

Common dev commands:
```bash
python -m black .
python -m ruff check .
python -m mypy griffin
python -m pytest -q
```

---

## 🧱 4. Layered Architecture (Code)

Top-level flow:
```
core  →  domain  →  services  →  ace  →  cli
           ↑          ↑
           └── infra ──┘
```

- core — atom types, pure utilities, FP helpers  
- domain — EVE + Griffin ontology (ships, systems, intel concepts)  
- infra — config, logging, DB, HTTP, secrets, telemetry  
- services — connectors (ESI/SDE), repositories, use-cases, analytics  
- ace — 6-layer cognitive engine (Aspirational → Task Prosecution)  
- cli — REPL, commands, renderers, TUI, visual modes

### 4.1 Hyper-Modular Directory Layout
```
griffin/
  ├─ core/ 
  ├─ domain/
  ├─ infra/
  ├─ services/
  ├─ ace/
  └─ cli/
```

### 4.2 Granularity Rules
- Directory = concept (noun)  
- File = single responsibility (verb/role)  
- Prefer 1 public class/function per file  
- `*_port.py` for interfaces; `*_impl.py` for adapters  
- Use `__init__.py` to re-export clean package APIs

---

## ⚛️ 5. Core Layer (Atoms)

- Pure, side-effect-free helpers, strongly typed IDs, quantities, time abstractions, base messaging primitives.  
- Time helpers use `python-dateutil`.  
- Messaging & boundaries use `pydantic` models.

---

## 🧠 6. Domain Layer (EVE Ontology)

- Pure domain: value_objects, entities, aggregates, services, specs.  
- Numeric heavy-lifting in combat/economy uses `numpy` / `scipy`.  
- Analytics use `pandas` for tabular operations.

---

## 🏗️ 7. Infra Layer (Ports & Adapters)

- HTTP: `infra/http/http_port.py` + `httpx` impl, backoff & rate-limiting wrappers (tenacity/backoff).  
- Logging: `loguru` behind `LoggingPort`.  
- Config: `pydantic` `AppConfig`.  
- Secrets: secret store port, file/OS-keyring impls.  
- Vector store: `chromadb` behind `VectorStorePort`.  
- Telemetry: `opentelemetry` wiring.

---

## 🔌 8. Services Layer

- Connectors: one ESI endpoint per file (sync for now, async later).  
- Mappers: ESI JSON → domain objects.  
- Repositories: persistence & caching (SQLite/Postgres via DBPort).  
- Sync jobs: periodic sync tasks (assets, markets, universe).  
- Use-cases: ACE-invokable actions (get_account_status, plan_asset_consolidation).  
- Analytics: portfolio/combat/risk using pandas/numpy/scipy + hypernetx for hypergraphs.

---

## 🧬 9. ACE Cognitive Architecture (6 Layers)

ACE embedded into G.R.I.F.F.I.N. with structured ACEMessages (Pydantic). Layers:

1. Aspirational — ethics, high-level mandates  
2. Global Strategy — world model, strategy selection  
3. Agent Model — capabilities & constraints (characters, skills, assets)  
4. Executive — project planning, resource allocation  
5. Cognitive Control — task selection, switching  
6. Task Prosecution — concrete actions via services/infra

ACE layers may use pure logic or LLM-backed reasoning (`simpleaichat`) with memory in `chromadb`.

---

## 🔺 10. ACE Layers Adapted to EVE (Concise)

- Aspirational: ethics, guardrails, high-level mandates  
- Strategy: region/regime strategy, trade & war posture  
- Agent Model: what you and the system can do (SP, assets, roles)  
- Executive: break strategies into projects with resources & risks  
- Control: schedule / select tasks responsive to live telemetry  
- Prosecution: perform tasks using ESI, DB, analytics

---

## 🛡️ 11. System Integrity Overlay

- Integrity monitor: token health, rate-limits, DB checks, model health.  
- Telemetry & traces via `opentelemetry`.  
- Health endpoints / CLI health-checks.

---

## 🧑‍✈️ 12. CLI & UI Layer

- CLI commands are mini-pipelines (parse → ACEMsg → ACE → use-case → render).  
- UX stack: `rich` (tables), `textual` (TUI), `asciimatics` (retro), `pygame` (experimental bridge).  
- All UI code kept behind rendering adapters.

---

## 🌐 13. SDE / ESI / G.R.I.F.F.I.N. Data Flow

- ESI: live telemetry — characters, wallets, fleets, markets, structures, notifications.  
- SDE: static universe topology, types, attributes.  
- G.R.I.F.F.I.N.: normalizes both into domain models, stores memory (chromadb), runs analytics, feeds ACE.

---

## 🔁 14. Example Vertical Slice — `griffin status`

1. CLI builds `StatusCommand` → `ACEMessage(kind="STATUS_QUERY")`  
2. ACE chooses tasks → prosecution calls `services/use_cases/get_account_status.py`  
3. Services call ESI via HTTPPort, map to domain, analytics compute net worth/risk  
4. Result rendered via `cli/render` using `rich`

---

## 📦 15. Key Packages & Where They Fit

- pydantic — schemas (infra/config, ACE messages)  
- python-dateutil — core time handling  
- httpx — HTTPPort / ESI connectors  
- loguru — logging_impl (infra/logging)  
- rich, textual, asciimatics, pygame — CLI/UI renderers  
- pandas, numpy, scipy — analytics & numeric services  
- hypernetx, networkx — graph/hypergraph analytics  
- simpleaichat, chromadb, huggingface_hub, onnxruntime — AI & memory stack

---

## ⛏️ 16. Implementation Order (First-Principles Build Plan)

Phase 1 — Skeleton & Tooling
- Create package layout with `__init__.py` in every package  
- Configure `black`, `ruff`, `mypy`, `pytest`  
- Add trivial test importing `griffin`

Phase 2 — Core & Infra Foundations
- Implement core ID/quantity/time/messaging modules  
- Implement `infra/config` (Pydantic AppConfig) and `loguru` wiring  
- Define ports: HTTPPort, DBPort, VectorStorePort, SecretStorePort

Phase 3 — ACE + CLI Skeleton
- Add `ace/core/ace_message.py` (Pydantic) and `ACEOrchestrator` stub  
- Add `cli/main.py` and REPL/one-shot plumbing  
- Verify CLI prints a live-ready banner

Phase 4 — Domain Modeling (No IO)
- Implement domain modules (identity, universe, inventory, combat)  
- Add pure unit tests for math/services

Phase 5 — ESI OAuth & Token Store
- Implement secret store and OAuth flow (Flask callback)  
- CLI `auth login` command to store tokens securely

Phase 6 — First Real Slice: `griffin whoami`
- Implement per-endpoint ESI connector, mapper, repo, use-case, CLI command  
- Wire ACE routing for WHOAMI

Phase 7 — Assets, Wallets, Markets, Fleets
- Repeat vertical slice pattern for main features and analytics

Phase 8 — Rich UI, TUI, AI Integration
- Enhance rendering with `rich` + `textual` TUI  
- Integrate `simpleaichat` + `chromadb` for ACE-backed LLM reasoning  
- Add hypergraph intel tooling with `hypernetx`

---

## 🔒 17. Secrets & Safety

- Never commit client IDs, secrets, access/refresh tokens.  
- Use `.env`, OS keyring, or encrypted file store.  
- Ensure automation recommendations remain within EULA.

---

## 🧪 18. Contributing

- Keep PRs small and mapped to layers.  
- Single responsibility per file, no circular deps.  
- Tests required for non-trivial logic.  
- Pre-commit: `black .`, `ruff check .`, `mypy griffin`, `pytest`.

---

## Appendix — Actions you can take now

- Drop this file as `ARCHITECTURE.md` (done).  
- Link it from `README.md` (optional).  
- When ready, I can:
  - create `Makefile` and CI pipeline,
  - pin versions and generate `constraints.txt` via `pip-tools`,
  - scaffold package directories and minimal stubs.

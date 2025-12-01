Below is your **fully rewritten README**, integrating:

* Everything from your original README
* The entire **hyper-modular architecture specification**
* ACE-layer topology
* SDE/ESI/GRIFFIN relationships
* Strict file granularity and naming conventions
* Vertical slice explanation
* Dependency flow
* Philosophy and design goals

**Formatted, structured, and ready for production.**
I **did not overwrite your existing content**—I expanded it into a complete, formal project document.

---

# 📘 **G.R.I.F.F.I.N.**

### **Galactic Recon & Intel Framework for Fleet Insight & Navigation**

**AI-enhanced EVE Online companion, intel engine, and multi-character orchestration system.**

---

# 🧠 1. Overview

G.R.I.F.F.I.N. is an advanced, modular EVE Online application designed to function as:

* A **shipboard AI copilot**
* A **fleet-aware strategic intel engine**
* An **account-wide economic & industrial brain**
* A **multi-character orchestration layer** for complex player operations
* A **CLI-driven AGI-like presence**, backed by the ACE reasoning framework

It integrates ESI + SDE + custom reasoning layers to deliver actionable intelligence, planning, analysis, and automation support for all your characters and corporations.

---

# 🧬 2. Current Project State

* **Python virtual environment:** `./.venv` (Python 3.12)
* **Directory root:** `E:\GRIFFIN`
* **Dependencies installed:** `black`, `pip`, `setuptools`, `wheel`
* **EVE Dev App:**

  * Name: **G.R.I.F.F.I.N.**
  * Callback: `eveauth-griffin://callback/`
  * All major ESI scopes granted (skillboard, wallet, intel, structures, fleets, markets, industry, etc.).

---

# 🧰 3. Developer Quickstart

## PowerShell

```powershell
Set-Location -LiteralPath 'E:\GRIFFIN'
. .\.venv\Scripts\Activate.ps1
python -V
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## cmd.exe

```bat
cd /d E:\GRIFFIN
```

## Dev Commands

* Format: `python -m black .`
* Tests: `python -m pytest -q`

---

# 🧱 4. High-Level Architecture

G.R.I.F.F.I.N. follows a **multi-layer architecture**, mapped to real EVE data sources (ESI/SDE) and an internal reasoning engine (ACE):

```
core → domain → services → ace → cli
          ↑        ↑
          └── infra ─┘
```

### In English:

* **Core** – atomic types (IDs, quantities, time, messaging, FP primitives)
* **Domain** – EVE ontology: ships, assets, universe, skills, markets, intel
* **Infra** – IO: DB, HTTP, config, cache, secrets
* **Services** – connectors (ESI, SDE), repositories, sync jobs, use-cases, analytics
* **ACE** – AGI-like cognition layer (6 layers) orchestrating requests & planning
* **CLI** – user interface to Griffin the AI companion

---

# 🧩 5. Full Hyper-Modular Directory Structure

*(Single-responsibility, single-function files; highly granular)*

```
  └─ griffin/
      ├─ core/ 
      │   ├─ ids/
      │   ├─ quantities/
      │   ├─ time/
      │   ├─ messaging/
      │   ├─ errors/
      │   ├─ fp/
      │   ├─ math/
      │   ├─ typing/
      │   └─ constants/
      │
      ├─ domain/
      │   ├─ common/
      │   ├─ identity/
      │   ├─ universe/
      │   ├─ items/
      │   ├─ inventory/
      │   ├─ combat/
      │   ├─ economy/
      │   ├─ intel/
      │   └─ planning/
      │
      ├─ infra/
      │   ├─ config/
      │   ├─ logging/
      │   ├─ db/
      │   ├─ http/
      │   ├─ cache/
      │   └─ security/
      │
      ├─ services/
      │   ├─ connectors/
      │   │   ├─ esi/
      │   │   └─ sde/
      │   ├─ mappers/
      │   ├─ repositories/
      │   ├─ sync/
      │   ├─ use_cases/
      │   └─ analytics/
      │
      ├─ ace/
      │   ├─ core/
      │   ├─ layers/
      │   └─ orchestrator/
      │
      └─ cli/
          ├─ parsing/
          ├─ commands/
          ├─ render/
          └─ modes/
```

---

# ⚛️ 6. The **Core Layer** (Atoms)

This is the “bedrock”—extremely granular, single-purpose files.

Examples:

## `core/ids/character_id.py`

```python
from typing import NewType
CharacterID = NewType("CharacterID", int)
```

## `core/quantities/isk_amount.py`

```python
from .numeric_base import Quantity
class ISK(Quantity):
    ...
```

Every ID/quantity/time primitive gets its own file and minimal helpers.

---

# 🧠 7. The **Domain Layer** (Ontology & Tautology)

Each bounded context has:

```
value_objects/
entities/
aggregates/
services/
specs/
```

Everything is **pure**—no IO, no side effects.

### Example: `domain/combat/`

```
combat/
  value_objects/
      resist_profile.py
      damage_profile.py
      tank_stats.py
      weapon_stats.py

  entities/
      ship_instance.py
      module_instance.py
      drone_instance.py

  aggregates/
      fit_profile.py

  services/
      compute_resists.py
      compute_ehp.py
      compute_dps.py
      evaluate_fit_role.py

  specs/
      high_tank_fit_spec.py
      high_dps_fit_spec.py
      logi_fit_spec.py
```

**One concept = one file.
One operation = one file.**

---

# 🏗️ 8. The **Infra Layer** (Ports & Adapters)

Every IO capability is split into:

* **Port** (Protocol)
* **Implementation**

Example:

```
infra/http/
  http_port.py
  requests_impl.py
  retry_decorator.py
  rate_limiter.py
  user_agent_builder.py
```

Example port:

```python
class HTTPPort(Protocol):
    def get(self, url: str, headers: dict) -> dict: ...
    def post(self, url: str, headers: dict, body: dict) -> dict: ...
```

---

# 🔌 9. The **Service Layer**

### 9.1 Connectors

**One ESI endpoint = one file.**

```
services/connectors/esi/characters/
  get_character_info.py
  get_character_skills.py
  get_character_skillqueue.py
  get_character_assets.py
  get_character_wallet.py
  get_character_orders.py
```

### 9.2 Mappers

```
services/mappers/esi_to_domain/characters/
  map_character_info.py
  map_character_skills.py
  map_character_assets.py
```

### 9.3 Repositories

```
repositories/
  repository_ports.py
  character_repo_impl.py
  asset_repo_impl.py
  market_repo_impl.py
```

### 9.4 Sync Tasks

```
sync/
  sync_characters.py
  sync_assets.py
  sync_universe.py
  sync_markets.py
```

### 9.5 Use-Cases

(ACE-triggerable actions)

```
use_cases/
  get_account_status.py
  get_fleet_snapshot.py
  plan_asset_consolidation.py
  get_market_overview.py
  get_industry_overview.py
```

### 9.6 Analytics

```
analytics/
  portfolio_analysis.py
  combat_analysis.py
  risk_analysis.py
```

---

# 🧬 10. The **ACE Cognitive Layer**

ACE consists of **six stacked layers**:

1. **Aspirational** – desires, goals, long-term aims  
2. **Strategy** – selecting strategies & global approaches  
3. **Agent Model** – reasoning about the world, characters, fleets  
4. **Executive** – selecting tasks and prioritizing actions  
5. **Control** – managing execution flow  
6. **Prosecution** – carrying out actions or queries

Structure:

```
ace/
  core/
    ace_message.py
    ace_state.py
    objectives.py
    tasks.py
    plans.py

  layers/
    base_layer.py
    aspirational_layer.py
    strategy_layer.py
    agent_model_layer.py
    executive_layer.py
    control_layer.py
    prosecution_layer.py

  orchestrator/
    wiring.py
    orchestrator.py
```

ACE receives `ACEMessage` objects from the CLI and returns resolved answers or commands.

---

# 🧑‍✈️ 11. The **CLI Layer**

User interacts with G.R.I.F.F.I.N. via a command-line AGI-like interface.

Structure:

```
cli/
  main.py
  app.py
  context.py
  session.py

  parsing/
    tokenize_input.py
    parse_tokens.py
    parse_flags.py

  commands/
    status/
       status_command.py
       build_status_request.py
       handle_status_response.py
       format_status_text.py

    fleet/
       fleet_command.py
       ...

  render/
    view_model_types.py
    render_view_model.py
    render_text.py
    render_table.py
    render_json.py

  modes/
    repl_mode.py
    one_shot_mode.py
    batch_mode.py
```

Each command is its own mini-pipeline.

---

# 🌐 12. How SDE, ESI, and G.R.I.F.F.I.N. Interact

### ESI

* Live character data
* Wallets
* Fleets
* Notifications
* Markets
* Structures
* Industry
* Corp roles & membership
* Skills & queues

### SDE

* Universe topology
* Ship & item types
* Attributes, effects, meta levels
* Categories, groups, markets
* Volumes, mass, capacity

### G.R.I.F.F.I.N.

* Fuses SDE + ESI into a unified ontology
* Maintains history + local cache
* Adds analytics, planning, reasoning
* Provides high-level insights through ACE
* Exposes human interaction via CLI

---

# 🔁 13. Example Full Vertical Slice (Status Command)

1. User enters:

   ```bash
   griffin status --char Ardemis
   ```

2. CLI parses input → `StatusCommand`.

3. CLI builds an `ACEMessage`.

4. ACE orchestrator routes through layers:

   * Strategy: determines info needed
   * Executive: selects tasks
   * Prosecution: executes get_account_status use-case

5. Service layer executes:

   * Repositories
   * Connectors
   * Analytics

6. Domain objects returned.

7. ACE wraps result → `STATUS_RESULT`.

8. CLI renderer prints beautiful table.

---

# 🔒 14. Notes on Secrets

* **Never commit secrets or client IDs.**
* Use `.env` or OS keychain via `infra/security/*`.

---

# 🧪 15. Contributing

* PRs welcome
* Keep all changes **small**, **atomic**, and **single-responsibility**
* Provide **tests** for every module

---

# 📚 16. Roadmap (Short)

1. Build full directory skeleton (empty files OK).
2. Add composition root for CLI + ACE.
3. Implement ESI OAuth + token refresh.
4. Implement fetchers + mappers for characters & assets.
5. Implement first ACE → CLI pipeline (“Status”).
6. Add dashboards, analytics, planning, and fleet intel.

---

# G.R.I.F.F.I.N.

Galactic Recon & Intel Framework for Fleet Insight & Navigation

G.R.I.F.F.I.N. is an EVE Online-focused intelligence companion and tool-suite: an AI-enhanced shipboard copilot, fleet-intel engine, and account-wide economic brain.

**Status — Snapshot (Nov 30, 2025)**
- Python virtual environment: `./.venv` (Python 3.12)
- Basic dev packages installed: `black`, `pip`, `setuptools`, `wheel` (see `requirements.txt`)
- EVE Dev App registration and scopes captured (full-spectrum read access)

**Project Goals (short)**
- Provide an OAuth-backed ESI client and local cache for character/corp data
- Offer a CLI and later a web/desktop UI for fleet & account intelligence
- Implement agent modules for real-time syntheses (notifications, killmails, market alerts)

**Repository layout (planned)**
```
E:\GRIFFIN
├─ .venv/
├─ griffin/         # python package (auth, esi_client, db, agents)
├─ scripts/         # helper scripts (bootstrap_venv.ps1)
├─ tests/
├─ docs/
├─ README.md
├─ requirements.txt
├─ pyproject.toml
└─ .gitignore
```

**Quick setup & activate (PowerShell)**

Open PowerShell and run:

```powershell
Set-Location -LiteralPath 'e:\GRIFFIN'
# Activate the project venv
. .\.venv\Scripts\Activate.ps1

# verify Python
python -V

# upgrade pip and install pinned deps
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

**Quick setup (cmd.exe)**

```
cd /d e:\GRIFFIN
e:\GRIFFIN\.venv\Scripts\activate.bat
```

**Developer commands**
- Format code: `python -m black .`
- Run tests (when present): `python -m pytest -q`

**What we have stored / confirmed**
- EVE Dev App registration with callback `eveauth-griffin://callback/` and extensive ESI scopes.
- Local venv at `e:\GRIFFIN\.venv` with core dev packages installed.

**Next recommended steps**
1. Create the package skeleton under `griffin/` (`__init__.py`, `auth.py`, `esi_client.py`, `db.py`).
2. Add `scripts/bootstrap_venv.ps1` to reproduce environment creation and dependency install.
3. Implement OAuth skeleton (placeholders safe for tracked secrets).

**Notes on secrets and configuration**
- Do not commit secrets or client credentials. Use an `.env` file (e.g. `.env.example`) and a secrets manager for real deployments.

**Contributing**
- Fork + PR. Keep changes small and focused. Add tests for new behavior.

**Contact / Maintainer**
- Project: G.R.I.F.F.I.N. — owner/maintainer contact details can be added here.

---

_README generated and expanded by the dev assistant on request._

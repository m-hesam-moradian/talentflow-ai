# TalentFlow-AI

> Autonomous Agentic Career & Document Orchestrator for the German Tech Market

TalentFlow-AI is an autonomous, agent-driven platform that orchestrates the
end-to-end job-search and application workflow for engineering talent targeting
the German tech market. It combines LLM-based reasoning, browser automation,
document generation, and structured persistence (Google Sheets) into a single
configurable runtime.

## Status

Project is currently in **Phase 0** (scaffolding & configuration baseline).
See [`ROADMAP.md`](./ROADMAP.md) for the full delivery plan.

## Tech Stack

- **Language:** Python 3.12+
- **Settings:** `pydantic-settings` with `.env` loading
- **LLM Orchestration:** `langgraph` + `litellm` (DeepSeek primary, Gemini fallback)
- **Browser Automation:** `playwright`
- **Document Generation:** `weasyprint` + `reportlab` + `jinja2`
- **Persistence:** `gspread` (Google Sheets)
- **Observability:** `langfuse`
- **Tooling:** `ruff`, `pytest`, `pytest-asyncio`

## Quick Start

```bash
# Install dependencies (editable + dev extras)
pip install -e ".[dev]"

# Configure environment
cp .env.example .env
# Edit .env with your API keys

# Run tests
pytest
```

## Project Layout

```
talentflow-ai/
├── src/              # Application source code
│   ├── config.py     # Pydantic-based settings module
│   └── __init__.py
├── tests/            # Unit and integration tests
│   └── test_config.py
├── .env.example      # Environment variable template
├── pyproject.toml    # Project metadata & tooling config
└── ROADMAP.md        # Phased delivery roadmap
```

## License

Proprietary — All rights reserved.

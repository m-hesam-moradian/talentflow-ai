# ROADMAP.md — Agentic Career Orchestrator (`talentflow-ai`)

> **🤖 AI CODING AGENT INSTRUCTIONS (READ FIRST — DO NOT SKIP):**
> 1. **Single Source of Truth:** This file is the stateful execution tracker and architectural specification for this repository. **Do not** re-analyze the entire repository from scratch on every session.
> 2. **How to Know Where to Start:** Look at the **Master Execution State Tracker** table immediately below. Find the **first phase/step** marked `[ ] PENDING` or `[~] IN_PROGRESS`.
> 3. **Execution Protocol:**
>    - Change the target step's status in the tracker table and phase checklist to `[~] IN_PROGRESS`.
>    - Create or update **only** the files listed under that step's **Deliverables**.
>    - Run the exact command listed under **Verification & Test Gate**.
>    - **Strict Gate Rule:** You may ONLY mark a step `[x] DONE` after its `pytest` / linter verification command exits with code `0`.
>    - Update `LAST_COMPLETED_STEP` and `NEXT_ACTIVE_STEP` in the State Header below before ending your turn.

---

## 📊 Master Execution State Tracker

- **PROJECT_STATUS:** `INITIALIZED`
- **LAST_COMPLETED_STEP:** `PHASE_0_STEP_1`
- **NEXT_ACTIVE_STEP:** `PHASE_0_STEP_2`
- **TARGET_PYTHON_VERSION:** `3.12+`
- **TARGET_NODE_VERSION:** `20+`

| Step ID | Phase & Task Name | Primary Tech | Target Directory / Files | Test Gate Command | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `PHASE_0_STEP_1` | Repo Scaffolding & Dependencies | `pyproject.toml`, `ruff`, `pytest` | `pyproject.toml`, `.env.example`, `src/__init__.py` | `pytest --version && ruff --version` | `[x] DONE` |
| `PHASE_0_STEP_2` | Strict Pydantic v2 Domain Schemas | `pydantic` v2 | `src/schemas/models.py`, `data/master_resume.json` | `pytest tests/test_schemas.py` | `[ ] PENDING` |
| `PHASE_1_STEP_1` | Multi-Source Germany Job Collectors | `httpx`, `beautifulsoup4` | `src/ingestion/collectors.py` | `pytest tests/test_collectors.py` | `[ ] PENDING` |
| `PHASE_1_STEP_2` | Deduplication, Visa Filter & Sheets Sync | `gspread`, `google-auth` | `src/ingestion/filter_engine.py`, `src/ingestion/sheets_client.py` | `pytest tests/test_ingestion_pipeline.py` | `[ ] PENDING` |
| `PHASE_2_STEP_1` | LiteLLM Router & Langfuse Tracing | `litellm`, `langfuse` | `src/gateway/llm_router.py` | `pytest tests/test_llm_router.py` | `[ ] PENDING` |
| `PHASE_3_STEP_1` | LangGraph State & Evaluator/Tailor Nodes | `langgraph`, `pydantic` | `src/agent/state.py`, `src/agent/nodes.py` | `pytest tests/test_agent_nodes.py` | `[ ] PENDING` |
| `PHASE_3_STEP_2` | Anti-Hallucination Guardrail & Cyclic Graph | `langgraph` | `src/agent/guardrails.py`, `src/agent/graph.py` | `pytest tests/test_hallucination_gate.py` | `[ ] PENDING` |
| `PHASE_4_STEP_1` | Model Context Protocol (MCP) Server | `mcp` (`FastMCP`) | `src/mcp_server/server.py` | `pytest tests/test_mcp_server.py` | `[ ] PENDING` |
| `PHASE_5_STEP_1` | 1-Page German ATS PDF Resume Compiler | `weasyprint` / `reportlab`, `jinja2` | `src/resume_engine/pdf_renderer.py`, `templates/cv_template.html` | `pytest tests/test_pdf_renderer.py` | `[ ] PENDING` |
| `PHASE_6_STEP_1` | Playwright ATS Auto-Applier Engine | `playwright` (Async) | `src/browser_bot/playwright_applier.py` | `pytest tests/test_playwright_applier.py` | `[ ] PENDING` |
| `PHASE_7_STEP_1` | Next.js Priority JSON Uploader (Vercel) | `Next.js 15`, `TypeScript`, `Tailwind` | `web/app/page.tsx`, `web/app/api/upload/route.ts` | `cd web && npm run build` | `[ ] PENDING` |
| `PHASE_8_STEP_1` | GitHub Actions CI/CD & 8 AM Cron Runner | `GitHub Actions`, `Docker` | `.github/workflows/ci.yml`, `.github/workflows/daily_agent.yml`, `src/main.py` | `pytest tests/ && ruff check src/` | `[ ] PENDING` |

---

## 🏗️ 1. System Architecture & Portfolio Goals

This project is an autonomous, production-grade **AI Career & Document Orchestrator** built for the German tech market (On-Site/Hybrid roles eligible for EU Blue Card or Visa Sponsorship). It is designed both as a daily personal automation system and as a flagship **MLOps / Agentic AI Engineering portfolio repository**.

### Core Engineering Pillars Demonstrated
1. **Dual-Track Ingestion (Zero LinkedIn Account Risk):**
   - **Track 1 (Automated Daily Cron):** Pulls directly from cookie-less public APIs: **Arbeitnow Germany API** (`.com` domain filter), **Bundesagentur für Arbeit Official API** (`X-API-Key: jobboerse-jobsuche`), **The Muse Germany API**, and **Direct Ashby / Greenhouse JSON Boards** (n8n, OpenAI Munich, Celonis, N26, SumUp, Raisin, GetYourGuide, Contentful).
   - **Track 2 (Priority Human-in-the-Loop Upload):** A Next.js web interface hosted on Vercel where exported Chrome Extension JSON files (`linkedin_selected_jobs.json`) are uploaded anytime and tagged as `0 - HIGH PRIORITY` in Google Sheets.
2. **Stateful Agentic Orchestration (`LangGraph`):**
   - Cyclic graph (`Ingest` $\rightarrow$ `EvaluateFitAndVisa` $\rightarrow$ `TailorResume` $\rightarrow$ `VerifyGroundTruthGuardrail` $\rightarrow$ `CompilePDF` $\rightarrow$ `AutoApply`).
   - Includes a self-correcting conditional edge: if the LLM invents any skill, tool, or job title not present in `data/master_resume.json`, the deterministic guardrail catches it and routes back to `TailorResume` with explicit error feedback.
3. **LLMOps Gateway & Observability (`LiteLLM` + `Langfuse`):**
   - Primary inference routed through OpenAI-compatible provider (Dahl / DeepSeek / MiniMax) with automatic zero-downtime fallback to Google Gemini (`gemini-2.5-flash`).
   - Full token cost, latency, and prompt/completion tracing logged to **Langfuse**.
4. **Standardized Tooling (`FastMCP`):**
   - Exposes sheet synchronization, job scoring, and PDF compilation as standardized **Model Context Protocol (MCP)** tools.
5. **Headless Browser Execution (`Playwright`):**
   - Fills single-page ATS portals (Greenhouse, Ashby, Personio, Join, Lever) on GitHub Actions' 7 GB RAM Ubuntu runner (or locally), uploads the tailored PDF CV, and updates the Google Sheet status to `Applied`.

### Target Repository Directory Tree
```text
talentflow-ai/
├── ROADMAP.md                          # Stateful execution spec (THIS FILE)
├── pyproject.toml                      # Python 3.12 dependencies, Ruff & Pytest config
├── .env.example                        # Template for all required environment variables
├── Dockerfile                          # Reproducible container image for agent execution
├── .github/
│   └── workflows/
│       ├── ci.yml                      # Runs Ruff + Pytest + Hallucination Gate on every push
│       └── daily_agent.yml             # Runs 8:00 AM daily cron + manual workflow_dispatch on 7GB RAM
├── data/
│   ├── master_resume.json              # Ground-truth candidate profile (verified skills, roles, education)
│   └── golden_eval_jobs.json           # 5 benchmark German job postings for CI evaluation tests
├── templates/
│   └── cv_template.html                # Clean 1-page German-standard ATS HTML/CSS resume template
├── src/
│   ├── __init__.py
│   ├── main.py                         # CLI & GitHub Actions entrypoint orchestrating the full pipeline
│   ├── config.py                       # Pydantic Settings environment loader
│   ├── schemas/
│   │   └── models.py                   # Pydantic v2 models (JobPosting, TailoredResume, EvalResult)
│   ├── ingestion/
│   │   ├── collectors.py               # Async fetchers for Arbeitnow, Bundesagentur, The Muse, Ashby, Greenhouse
│   │   ├── filter_engine.py            # Regex & rule engine (Germany location, title match, C2/visa blocker)
│   │   └── sheets_client.py            # Google Sheets API v4 append/update/fetch with priority sorting
│   ├── gateway/
│   │   └── llm_router.py               # LiteLLM wrapper with Primary -> Gemini fallback + Langfuse decorator
│   ├── agent/
│   │   ├── state.py                    # LangGraph TypedDict state definition
│   │   ├── nodes.py                    # EvaluatorNode, TailorNode, PDFNode, ApplyNode
│   │   ├── guardrails.py               # Deterministic Ground-Truth Judge (0% hallucination check)
│   │   └── graph.py                    # Compiled LangGraph StateGraph with conditional retry edges
│   ├── mcp_server/
│   │   └── server.py                   # FastMCP server exposing agent capabilities as MCP tools
│   ├── resume_engine/
│   │   └── pdf_renderer.py             # Renders TailoredResume + Jinja2 HTML into 1-page PDF
│   └── browser_bot/
│       └── playwright_applier.py       # Async Playwright DOM filler for Ashby, Greenhouse, Personio
├── tests/
│   ├── conftest.py                     # Shared fixtures (mock jobs, master resume, mock LLM responses)
│   ├── test_schemas.py
│   ├── test_collectors.py
│   ├── test_ingestion_pipeline.py
│   ├── test_llm_router.py
│   ├── test_agent_nodes.py
│   ├── test_hallucination_gate.py
│   ├── test_mcp_server.py
│   ├── test_pdf_renderer.py
│   └── test_playwright_applier.py
└── web/                                # Next.js 15 App (Deployed on Vercel)
    ├── package.json
    ├── app/
    │   ├── page.tsx                    # Drag-and-drop Priority Extension JSON uploader + status table
    │   └── api/
    │       └── upload/
    │           └── route.ts            # Parses uploaded JSON, writes `0 - HIGH PRIORITY` to Google Sheets, triggers GitHub Action
```

---

## 🚀 2. Step-by-Step Implementation Phases

---

### PHASE 0: Repository Scaffolding, Config & Strict Domain Schemas

#### [x] `PHASE_0_STEP_1`: Repo Scaffolding & Dependencies
- **Goal:** Initialize the Python 3.12 project, virtual environment configuration, linter (`ruff`), test runner (`pytest`), and environment variable loader.
- **Deliverables:**
  1. `pyproject.toml`: Include dependencies: `pydantic>=2.7`, `pydantic-settings>=2.2`, `httpx>=0.27`, `beautifulsoup4>=4.12`, `gspread>=6.1`, `google-auth>=2.29`, `langgraph>=0.2`, `litellm>=1.40`, `langfuse>=2.36`, `mcp>=1.0`, `jinja2>=3.1`, `weasyprint>=62.0` (or `reportlab>=4.2` fallback), `playwright>=1.45`, and dev dependencies `pytest>=8.2`, `pytest-asyncio>=0.23`, `respx>=0.21`, `ruff>=0.5`.
  2. `.env.example`: Document keys (`PRIMARY_LLM_API_KEY`, `PRIMARY_LLM_BASE_URL`, `PRIMARY_LLM_MODEL`, `GEMINI_API_KEY`, `LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY`, `LANGFUSE_HOST`, `GOOGLE_SHEET_ID`, `GOOGLE_SERVICE_ACCOUNT_JSON`, `GITHUB_PAT_TOKEN`).
  3. `src/config.py`: Implement `Settings(BaseSettings)` using `pydantic-settings` with sensible defaults so unit tests run even without live API keys.
- **Verification & Test Gate:**
  ```bash
  pip install -e ".[dev]"
  ruff check src/
  pytest --version
  ```
- **Done Criteria:** Dependencies install cleanly and `ruff check src/` returns 0 errors.

#### [ ] `PHASE_0_STEP_2`: Strict Pydantic v2 Domain Schemas & Master Resume Ground Truth
- **Goal:** Define immutable data contracts for job listings, master resume ground truth, and LLM structured outputs.
- **Deliverables:**
  1. `data/master_resume.json`: Ground-truth JSON containing candidate's real personal info, education, work history (exact company names, titles, dates), project portfolio, languages, and `all_verified_skills` array.
  2. `src/schemas/models.py`:
     - `JobPriority(str, Enum)`: `HIGH_EXTENSION = "0 - HIGH PRIORITY | Manual Extension Upload"`, `DIRECT_ATS = "1 - DIRECT ATS"`, `NORMAL_API = "2 - NORMAL API"`.
     - `JobPosting(BaseModel)`: `id`, `source`, `title`, `company`, `location`, `work_mode`, `visa_status`, `seniority`, `employment_type`, `salary`, `posted_at`, `url`, `emails`, `description`, `found_at`, `application_status` (default `"Pending"`).
     - `JobEvaluation(BaseModel)`: `should_apply: bool`, `match_score: int = Field(ge=0, le=100)`, `visa_assessment: str`, `reasoning: str`, `missing_critical_skills: list[str]`.
     - `TailoredResumeOutput(BaseModel)`: `selected_headline: str`, `executive_summary: str`, `selected_skills: list[str]`, `tailored_experience_bullets: dict[str, list[str]]` (keyed by exact company ID from `master_resume.json`), `cover_letter_text: str`.
  3. `tests/test_schemas.py`: Unit tests validating schema serialization, invalid score rejection (`match_score=105` raises `ValidationError`), and loading `data/master_resume.json`.
- **Verification & Test Gate:**
  ```bash
  pytest tests/test_schemas.py -v
  ```
- **Done Criteria:** All schema validation tests pass (`exit 0`).

---

### PHASE 1: Multi-Source German Job Ingestion & Google Sheets Sync

#### [ ] `PHASE_1_STEP_1`: Multi-Source Germany Job Collectors (Cookie-Less APIs)
- **Goal:** Build async HTTP collectors that fetch fresh German tech jobs without touching LinkedIn login sessions or exceeding 50 MB of RAM.
- **Deliverables:**
  1. `src/ingestion/collectors.py`:
     - `fetch_arbeitnow_germany(client: httpx.AsyncClient) -> list[JobPosting]`: Calls `https://www.arbeitnow.com/api/job-board-api?visa_sponsorship=true` AND `?page=1`. Strictly filters `url` to `"arbeitnow.com"` (blocking `.nl`, `.fr`, `.co.uk`, `.ch`) and `remote == False`.
     - `fetch_bundesagentur_germany(client: httpx.AsyncClient) -> list[JobPosting]`: Calls `https://rest.arbeitsagentur.de/jobboerse/jobsuche-service/pc/v4/jobs` with header `X-API-Key: jobboerse-jobsuche` and params `was=AI Engineer Software Engineer`, `wo=Deutschland`, `veroeffentlichtseit=2`, `zeitarbeit=false`, `pav=false`.
     - `fetch_themuse_germany(client: httpx.AsyncClient) -> list[JobPosting]`: Calls `https://www.themuse.com/api/public/jobs` for `Berlin, Germany` and `Munich, Germany` in `Software Engineering` and `Data and Analytics`.
     - `fetch_direct_ats_boards(client: httpx.AsyncClient) -> list[JobPosting]`: Queries lightweight public JSON endpoints for German offices on Ashby (`api.ashbyhq.com/posting-api/job-board/{board}` for `n8n`, `langdock`) and Greenhouse (`boards-api.greenhouse.io/v1/boards/{board}/jobs` for `celonis`, `n26`, `sumup`, `raisin`), filtering strictly to German cities before parsing descriptions.
     - `parse_extension_json(raw_json_bytes: bytes) -> list[JobPosting]`: Converts uploaded Chrome Extension JSON into `JobPosting` objects with `source = JobPriority.HIGH_EXTENSION`.
  2. `tests/test_collectors.py`: Uses `respx` or `unittest.mock` to mock API responses and verify HTML entity unescaping (`&lt;p&gt;` $\rightarrow$ clean text), `.nl`/`.fr` domain blocking, and `JobPosting` normalization.
- **Verification & Test Gate:**
  ```bash
  pytest tests/test_collectors.py -v
  ```
- **Done Criteria:** All 5 collector parsers pass unit tests using mocked HTTP fixtures.

#### [ ] `PHASE_1_STEP_2`: Deterministic Filter Engine, Deduplication & Google Sheets Client
- **Goal:** Filter out non-engineering titles and visa blockers, deduplicate across sources, and sync with Google Sheets (`N8N - Sheet1`).
- **Deliverables:**
  1. `src/ingestion/filter_engine.py`:
     - `TITLE_INCLUDE_REGEX`: Matches AI, ML, Deep Learning, LLM, GenAI, Agentic, Full-Stack, Software Engineer, Backend, Python, TypeScript, Forward Deployed.
     - `TITLE_EXCLUDE_REGEX`: Rejects Product Manager, Public Affairs, Customer Success, Service Designer, Marketing, Sales, Recruiter, HR, Working Student, Intern, Praktikum, Werkstudent.
     - `VISA_BLOCKER_REGEX`: Rejects descriptions containing *"Arbeitserlaubnis für Deutschland erforderlich"*, *"EU citizenship required"*, *"no visa sponsorship"*, *"C2 German required"*, or *"native-level German proficiency is required"*.
     - `deduplicate_jobs(jobs: list[JobPosting], existing_ids: set[str]) -> list[JobPosting]`: Deduplicates by `id` AND normalized `(title.lower(), company.lower())`, keeping highest-priority source first (`0 - HIGH PRIORITY` > `1 - DIRECT ATS` > `2 - NORMAL API`).
  2. `src/ingestion/sheets_client.py`:
     - `GoogleSheetsRepo`: Uses `gspread` service account / OAuth credentials to fetch existing `id` column values, append new deduplicated `JobPosting` rows matching the 16-column schema (`id`, `source`, `title`, `company`, `location`, `workMode`, `visaStatus`, `seniority`, `employmentType`, `salary`, `applicants`, `postedAt`, `url`, `emails`, `description`, `foundAt`), and fetch unprocessed rows sorted by `source` ascending (`0 - HIGH PRIORITY` first).
  3. `tests/test_ingestion_pipeline.py`: Tests regex filtering (ensuring *"Public Affairs, Head of Germany"* and *"Senior Product Manager"* are rejected while *"Senior Fullstack AI Engineer"* passes), deduplication, and mocked Google Sheets batch append.
- **Verification & Test Gate:**
  ```bash
  pytest tests/test_ingestion_pipeline.py -v
  ```
- **Done Criteria:** Filter, deduplication, and sheet sync tests pass with 100% accuracy.

---

### PHASE 2: AI Gateway, Model Routing & Observability (`LiteLLM` + `Langfuse`)

#### [ ] `PHASE_2_STEP_1`: Resilient LLM Router with Automatic Fallback & Tracing
- **Goal:** Create a unified LLM gateway that calls the primary model (Dahl / MiniMax / DeepSeek), automatically falls back to Gemini (`gemini-2.5-flash`) on timeout/rate-limit, enforces Pydantic v2 structured JSON output, and logs traces to Langfuse.
- **Deliverables:**
  1. `src/gateway/llm_router.py`:
     - `LLMGateway`: Wraps `litellm.acompletion` (or `Router`) with `@observe()` from `langfuse.decorators`.
     - Method `async def generate_structured(prompt: str, system_prompt: str, response_model: type[T]) -> T`: Attempts primary model; if an `APIError`, `RateLimitError`, or `ValidationError` occurs, automatically retries with fallback model (`gemini/gemini-2.5-flash`) and validates output via `response_model.model_validate_json()`.
  2. `tests/test_llm_router.py`: Tests primary model success, simulates a `503 ServiceUnavailable` on the primary provider to verify seamless fallback to Gemini, and verifies Pydantic parsing.
- **Verification & Test Gate:**
  ```bash
  pytest tests/test_llm_router.py -v
  ```
- **Done Criteria:** Primary execution and automatic fallback tests pass.

---

### PHASE 3: LangGraph Stateful Agent & Anti-Hallucination Guardrail

#### [ ] `PHASE_3_STEP_1`: LangGraph State & Evaluator / Resume Tailor Nodes
- **Goal:** Build the core LangGraph nodes that evaluate job fit/visa eligibility and tailor the candidate's resume to the target German job description.
- **Deliverables:**
  1. `src/agent/state.py`: Define `CareerAgentState(TypedDict)` containing `job: JobPosting`, `master_resume: dict`, `evaluation: Optional[JobEvaluation]`, `tailored_resume: Optional[TailoredResumeOutput]`, `hallucination_errors: list[str]`, `retry_count: int`, `pdf_path: Optional[str]`, `apply_status: str`.
  2. `src/agent/nodes.py`:
     - `evaluate_job_node(state: CareerAgentState) -> dict`: Scores job (`0-100`) against `master_resume` and checks EU Blue Card / visa sponsorship compatibility.
     - `tailor_resume_node(state: CareerAgentState) -> dict`: Rewrites executive summary, selects relevant subset of skills from `master_resume["all_verified_skills"]`, reframes experience bullets to highlight matching German JD keywords (e.g., MLOps, LangGraph, React, Next.js, Python, Docker, CI/CD), and drafts a concise cover letter. If `state["hallucination_errors"]` is non-empty, injects those exact errors into the prompt for self-correction.
  3. `tests/test_agent_nodes.py`: Tests `evaluate_job_node` and `tailor_resume_node` using deterministic mock LLM outputs.
- **Verification & Test Gate:**
  ```bash
  pytest tests/test_agent_nodes.py -v
  ```
- **Done Criteria:** Node unit tests pass.

#### [ ] `PHASE_3_STEP_2`: Deterministic Ground-Truth Guardrail & Cyclic LangGraph Compilation
- **Goal:** Implement the LLMOps anti-hallucination quality gate and wire the cyclic `StateGraph`.
- **Deliverables:**
  1. `src/agent/guardrails.py`:
     - `verify_ground_truth_node(state: CareerAgentState) -> dict`: Deterministically checks `state["tailored_resume"]` against `state["master_resume"]`:
       1. Every skill in `selected_skills` must exist (case-insensitive) in `master_resume["all_verified_skills"]`.
       2. Every company key in `tailored_experience_bullets` must match an authentic company ID in `master_resume["experience"]`.
       3. Bullet count per role must not exceed limits, and no forbidden fabricated keywords may appear.
       Returns `hallucination_errors: list[str]` and increments `retry_count`.
  2. `src/agent/graph.py`:
     - Compiles the `StateGraph(CareerAgentState)`:
       - `evaluate_job` $\rightarrow$ conditional edge (`match_score >= 70 and should_apply` $\rightarrow$ `tailor_resume`, else $\rightarrow$ `END` with `"Skipped"`).
       - `tailor_resume` $\rightarrow$ `verify_ground_truth`.
       - `verify_ground_truth` $\rightarrow$ conditional edge:
         - If `len(hallucination_errors) == 0` $\rightarrow$ proceed to `compile_pdf`.
         - If `len(hallucination_errors) > 0 and retry_count <= 2` $\rightarrow$ loop back to `tailor_resume`.
         - If `retry_count > 2` $\rightarrow$ strip unverified skills deterministically and proceed to `compile_pdf`.
  3. `tests/test_hallucination_gate.py`:
     - Test 1: Injects a fake skill (`"Kubernetes Certified Administrator"` or `"Rust"`) not in `master_resume.json` and verifies `verify_ground_truth_node` flags it and triggers the self-correction loop in `graph.py`.
     - Test 2: Verifies a low-scoring job (`match_score = 45`) routes directly to `Skipped` without calling the Tailor LLM.
- **Verification & Test Gate:**
  ```bash
  pytest tests/test_hallucination_gate.py -v
  ```
- **Done Criteria:** Cyclic retry loop and hallucination rejection tests pass.

---

### PHASE 4: Model Context Protocol (MCP) Server Integration

#### [ ] `PHASE_4_STEP_1`: FastMCP Server Exposing Career Orchestrator Tools
- **Goal:** Expose the pipeline's core capabilities via Anthropic's **Model Context Protocol (`FastMCP`)** so external MCP clients (Claude Desktop, Cursor, or enterprise agent harnesses) can invoke them natively.
- **Deliverables:**
  1. `src/mcp_server/server.py`:
     - Uses `from mcp.server.fastmcp import FastMCP` (`mcp = FastMCP("TalentFlow-Career-Orchestrator")`).
     - `@mcp.tool() async def collect_german_jobs() -> dict`: Runs the multi-source Germany collectors and returns count of newly added jobs.
     - `@mcp.tool() async def evaluate_and_tailor_job(job_id: str) -> dict`: Runs the compiled LangGraph workflow on a specific `job_id` and returns the structured `TailoredResumeOutput` + guardrail report.
     - `@mcp.tool() async def list_priority_jobs(limit: int = 10) -> list[dict]`: Returns top pending jobs sorted by priority (`0 - HIGH PRIORITY` first).
  2. `tests/test_mcp_server.py`: Tests direct invocation of all 3 MCP tool functions with mocked dependencies.
- **Verification & Test Gate:**
  ```bash
  pytest tests/test_mcp_server.py -v
  ```
- **Done Criteria:** All MCP tools return valid JSON payloads and pass `pytest`.

---

### PHASE 5: German-Standard 1-Page ATS PDF Resume & Cover Letter Engine

#### [ ] `PHASE_5_STEP_1`: HTML/Jinja2 to 1-Page PDF Compiler
- **Goal:** Render the verified `TailoredResumeOutput` + `master_resume.json` metadata into a clean, single-page, ATS-parsable PDF (`output/Moradian_Hesam_{Company}_CV.pdf`).
- **Deliverables:**
  1. `templates/cv_template.html`: Clean, single-page A4 CSS layout (0.4in margins, crisp sans-serif typography, zero multi-column tables that break ATS parsers, bold metric highlights).
  2. `src/resume_engine/pdf_renderer.py`:
     - `render_resume_pdf(master_resume: dict, tailored: TailoredResumeOutput, company: str, output_dir: Path) -> Path`: Renders Jinja2 HTML template and compiles to PDF via `weasyprint` (with pure-Python `reportlab` fallback if system Cairo/Pango libraries are absent on Windows).
  3. `tests/test_pdf_renderer.py`: Generates a test PDF in `tmp_path`, asserts file exists, asserts file size `> 1000` bytes, and verifies `%PDF-` magic header bytes.
- **Verification & Test Gate:**
  ```bash
  pytest tests/test_pdf_renderer.py -v
  ```
- **Done Criteria:** Test produces a valid `%PDF` binary artifact and passes `pytest`.

---

### PHASE 6: Playwright Headless ATS Auto-Applier

#### [ ] `PHASE_6_STEP_1`: Async Playwright DOM Auto-Applier for Ashby, Greenhouse & Personio
- **Goal:** Automate form filling and PDF resume upload on direct company ATS portals without crashing memory, supporting both `DRY_RUN=true` (fills form + saves screenshot without clicking final Submit) and `DRY_RUN=false` (submits application).
- **Deliverables:**
  1. `src/browser_bot/playwright_applier.py`:
     - `ATSAutoApplier`: Launches headless Chromium with `--disable-dev-shm-usage` (prevents Docker/Linux shared memory crashes).
     - Detects portal type (`greenhouse.io`, `ashbyhq.com`, `personio.de`, `join.com`, `lever.co`, or generic form).
     - Populates First Name, Last Name, Email, Phone, LinkedIn URL, GitHub/Portfolio URL, Salary Expectation, and Notice Period from `master_resume.json`.
     - Uploads the generated `Moradian_Hesam_{Company}_CV.pdf` to `<input type="file">`.
     - Saves a verification screenshot to `artifacts/screenshots/{job_id}.png`.
     - If `dry_run=False`, submits the form and returns `ApplicationResult(status="Applied", screenshot_path=...)`; if login wall / CAPTCHA is detected, returns `ApplicationResult(status="Manual Action Needed - Tailored PDF Ready")`.
  2. `tests/test_playwright_applier.py`: Spins up a local mock HTML ATS form (`<form>` with name, email, resume file input, cover letter textarea, and submit button), runs `ATSAutoApplier` against it, and verifies all fields and the PDF upload are populated accurately.
- **Verification & Test Gate:**
  ```bash
  playwright install chromium
  pytest tests/test_playwright_applier.py -v
  ```
- **Done Criteria:** Local HTML ATS form test passes with file upload and screenshot verification.

---

### PHASE 7: Next.js Priority JSON Uploader & Command Dashboard (Vercel)

#### [ ] `PHASE_7_STEP_1`: Next.js 15 App for Anytime Chrome Extension JSON Uploads
- **Goal:** Provide an always-on, zero-crash web interface on Vercel where the user can drag-and-drop `linkedin_selected_jobs.json` from their Chrome Extension anytime, push those jobs to Google Sheets as `0 - HIGH PRIORITY`, and optionally trigger the GitHub Actions auto-apply workflow via webhook.
- **Deliverables:**
  1. `web/package.json`, `web/tsconfig.json`, `web/next.config.mjs`.
  2. `web/app/page.tsx`: Clean dashboard featuring:
     - Drag-and-drop `.json` file upload zone for Chrome Extension exports.
     - Live preview table showing parsed jobs before/after upload.
     - "Sync to Google Sheets (`0 - HIGH PRIORITY`) & Trigger Agent" button.
  3. `web/app/api/upload/route.ts`: Next.js API Route that validates the uploaded JSON array, prefixes every job with `source: "0 - HIGH PRIORITY | Manual Extension Upload"`, appends them to Google Sheets via Google Sheets REST API, and sends a `POST` request to GitHub's `actions/workflows/daily_agent.yml/dispatches` endpoint so the 7 GB RAM GitHub runner immediately tailors and applies to those priority jobs.
- **Verification & Test Gate:**
  ```bash
  cd web && npm install && npm run build
  ```
- **Done Criteria:** `npm run build` succeeds with zero TypeScript or Next.js build errors.

---

### PHASE 8: MLOps CI/CD Pipelines & End-to-End Entrypoint

#### [ ] `PHASE_8_STEP_1`: CLI Orchestrator, GitHub Actions CI Gate & Daily 8 AM Cron Runner
- **Goal:** Wire the entire Python pipeline into `src/main.py` and configure GitHub Actions for Continuous Integration (`ci.yml`) and Daily Autonomous Execution (`daily_agent.yml`).
- **Deliverables:**
  1. `src/main.py`: CLI entrypoint supporting flags:
     - `python -m src.main --mode collect` (Runs Phase 1 collectors + deduplication + Google Sheets sync).
     - `python -m src.main --mode process --max-jobs 10 --dry-run` (Fetches top pending rows from Google Sheets with `0 - HIGH PRIORITY` first, runs LangGraph Evaluator $\rightarrow$ Tailor $\rightarrow$ Guardrail $\rightarrow$ PDF $\rightarrow$ Playwright Applier, and updates Google Sheets status).
     - `python -m src.main --mode full` (Runs `collect` followed by `process`).
  2. `.github/workflows/ci.yml`: Triggers on `push` and `pull_request` to `main`. Runs `ruff check src/` and `pytest tests/ -v --cov=src`.
  3. `.github/workflows/daily_agent.yml`: Triggers on `schedule: - cron: '0 7 * * *'` (8:00 AM CET) and `workflow_dispatch`. Installs Python 3.12 + Playwright Chromium on `ubuntu-latest` (7 GB RAM), runs `python -m src.main --mode full`, and uploads generated PDF resumes and Playwright screenshots as downloadable GitHub Workflow Artifacts (`retention-days: 14`).
  4. `README.md`: Executive-grade portfolio documentation featuring system architecture diagrams, MLOps guardrail benchmarks, MCP tool documentation, and setup instructions for recruiters and hiring managers.
- **Verification & Test Gate:**
  ```bash
  ruff check src/ tests/
  pytest tests/ -v
  python -m src.main --help
  ```
- **Done Criteria:** Entire test suite (`pytest tests/`) and linter (`ruff check`) pass with 0 errors, and all rows in the **Master Execution State Tracker** at the top of `ROADMAP.md` are marked `[x] DONE`.
# AIBE v2.0 — Improved Implementation Plan

## Audit of Existing Codebase

### What Exists (Phase 0 — ~70% complete)

| File | Lines | Status |
|---|---|---|
| [pyproject.toml](file:///c:/Users/ADRIANO/AIDA/pyproject.toml) | 108 | ✅ Good |
| [docker-compose.yml](file:///c:/Users/ADRIANO/AIDA/docker-compose.yml) | 281 | ⚠️ Has issue |
| [Makefile](file:///c:/Users/ADRIANO/AIDA/Makefile) | 52 | ✅ Good |
| [Dockerfile.backend](file:///c:/Users/ADRIANO/AIDA/Dockerfile.backend) | 30 | ⚠️ Has issue |
| [Dockerfile.frontend](file:///c:/Users/ADRIANO/AIDA/Dockerfile.frontend) | 32 | ✅ Good |
| [.pre-commit-config.yaml](file:///c:/Users/ADRIANO/AIDA/.pre-commit-config.yaml) | 50 | ✅ Good |
| [ruff.toml](file:///c:/Users/ADRIANO/AIDA/ruff.toml) | 39 | ⚠️ Has issue |
| [mypy.ini](file:///c:/Users/ADRIANO/AIDA/mypy.ini) | 59 | ✅ Good |
| [env.example](file:///c:/Users/ADRIANO/AIDA/env.example) | 172 | ✅ Good |
| [.python-version](file:///c:/Users/ADRIANO/AIDA/.python-version) | 1 | ✅ |
| [.gitignore](file:///c:/Users/ADRIANO/AIDA/.gitignore) | 59 | ✅ Good |
| [ci.yml](file:///c:/Users/ADRIANO/AIDA/.github/workflows/ci.yml) | 115 | ✅ Good |
| [cd.yml](file:///c:/Users/ADRIANO/AIDA/.github/workflows/cd.yml) | 27 | ⚠️ Has issue |

Empty directories exist: `aibe/core/browser/`, `aibe/core/memory/`, `aibe/core/message_bus/`, `aibe/core/orchestrator/`, `aibe/core/vm_manager/`.

**Zero Python source files exist.** Phases 1–9 are entirely unstarted.

### Bugs Found in Existing Files

> [!CAUTION]
> These 5 issues must be fixed before proceeding to Phase 1.

#### Bug 1: `ruff.toml` — misplaced top-level keys
`line-length` and `target-version` are nested under `[lint]` but ruff expects them at root level. This means ruff silently ignores them and uses defaults (88 / no target).

```diff
+line-length = 88
+target-version = "py312"
+
 [lint]
-line-length = 88
-target-version = "py312"
```

#### Bug 2: `Dockerfile.backend` — broken install command
`uv pip install --system --no-cache -r pyproject.toml` is not valid — `uv` cannot use `pyproject.toml` as a `-r` requirements file. Must install the project itself.

```diff
 COPY pyproject.toml ./
-RUN uv pip install --system --no-cache -r pyproject.toml
+COPY aibe/ ./aibe/
+RUN uv pip install --system --no-cache "."
```
Also remove the later duplicate `COPY aibe/ ./aibe/` line.

#### Bug 3: `docker-compose.yml` — deprecated `version` key
Docker Compose v2+ ignores the `version:` key and emits a warning. Remove it.

```diff
-version: "3.9"
-
 x-common-env: &common-env
```

#### Bug 4: `cd.yml` — empty `needs`, should gate on CI
The deploy job has `needs: []` so it runs without waiting for CI. Should reference the CI workflow or at minimum have its own checks.

```diff
-    needs: []
+    needs: []  # TODO: add CI check reference once workflow_run is configured
```
*(Leave as-is for now but add the comment — proper fix requires `workflow_run` trigger or reusable workflows.)*

#### Bug 5: `env.example` — filename mismatch
The file is `env.example` but `Makefile` references `.env.example` and `.gitignore` expects `.env.example`. Rename to `.env.example`.

---

## What's Missing from Phase 0

- `setup.ps1` / `setup.sh` — one-command bootstrap scripts
- `docker-compose.override.yml` — dev volume mounts, hot-reload
- `scripts/` directory — `validate_env.py`, `wait_for_services.py`, `health_check.py`, `init_nats.py`, `init_vault.py`
- `terraform/` skeleton — networking, compute, databases modules
- `aibe/config/` — `agents.yaml`, `routing_table.yaml`, `kpi_thresholds.yaml`, `security_policies.yaml`, `budget.yaml`
- All `__init__.py` files throughout `aibe/`
- Full directory tree per spec (30+ subdirectories missing)
- `alembic.ini` + `alembic/` (referenced by Dockerfile but doesn't exist)

---

## Improved Phase Plan

> [!IMPORTANT]
> **Key changes from original plan:**
> 1. **Phase 0 completion** split out as explicit first step — fix bugs, fill gaps
> 2. **Phase 1 reordered** — config/types/exceptions/logging FIRST (everything depends on them), then DB, then bus/memory/router/etc.
> 3. **`__init__.py` strategy** — every package gets a proper `__init__.py` with explicit `__all__` exports, created as we build each module (not all at once)
> 4. **Phases 3 agents grouped by dependency** — Tier 0 first (others depend on Oracle decisions), then tiers can parallelize
> 5. **Verification per phase** — concrete `pytest` / `mypy` / `ruff` commands at each step, not just at the end
> 6. **Phase 6 (3D) descoped** — build the 2D Agent Universe (React Flow) first as Phase 5, then 3D as Phase 6 enhancement. This unblocks the dashboard much earlier.

---

### Phase 0 — Complete Skeleton & Fix Bugs
**Goal**: Bootable project structure with zero broken configs.

#### [MODIFY] Fixes to existing files
- [ruff.toml](file:///c:/Users/ADRIANO/AIDA/ruff.toml) — move `line-length`/`target-version` to root
- [Dockerfile.backend](file:///c:/Users/ADRIANO/AIDA/Dockerfile.backend) — fix `uv` install command
- [docker-compose.yml](file:///c:/Users/ADRIANO/AIDA/docker-compose.yml) — remove `version: "3.9"`
- [cd.yml](file:///c:/Users/ADRIANO/AIDA/.github/workflows/cd.yml) — add TODO comment on `needs`
- Rename `env.example` → `.env.example`

#### [NEW] Missing scaffold files
- `setup.ps1` — PowerShell bootstrap (install uv, sync, copy .env, install pre-commit)
- `setup.sh` — Bash equivalent
- `docker-compose.override.yml` — dev volume mounts, `--reload` flags
- `alembic.ini` + `aibe/core/db/migrations/env.py` + `versions/`
- `aibe/__init__.py` — root package init
- `aibe/core/__init__.py`

#### [NEW] Config YAML files
- `aibe/config/agents.yaml` — 35 agent definitions (id, name, tier, default_task_type, allowed_task_types, daily_budget_usd)
- `aibe/config/routing_table.yaml` — 9 task types with primary/fallback models and cost rates
- `aibe/config/kpi_thresholds.yaml` — KPI targets per business metric
- `aibe/config/security_policies.yaml` — scan schedules, severity gates, rotation periods
- `aibe/config/budget.yaml` — global and per-agent budget limits

#### [NEW] Utility scripts
- `scripts/validate_env.py` — check all required env vars are set
- `scripts/wait_for_services.py` — poll healthchecks before app startup
- `scripts/health_check.py` — comprehensive service health reporter

#### [NEW] Full directory tree
Create all `aibe/` subdirectories per spec (with empty `__init__.py` as placeholder where needed):
```
aibe/
├── __init__.py
├── core/           (+ __init__.py for all sub-packages below)
│   ├── config.py, types.py, exceptions.py, logging.py
│   ├── orchestrator/
│   ├── message_bus/
│   ├── memory/
│   ├── browser/
│   ├── vm_manager/
│   ├── router/
│   ├── secret_vault/
│   ├── cost_tracker/
│   ├── db/
│   └── tools/
├── agents/
│   ├── base/, delegation/, meetings/
│   ├── executive/, research/, product/, marketing/, social/
│   ├── finance/, evolution/, ai_ml/, security/, sales/
│   └── registry.py
├── security/
├── ml_pipeline/
├── contractor/
├── sales_engine/
├── task_delegation/
├── tools/
├── config/
├── workers/
├── ui/
│   ├── backend/
│   └── frontend/
├── infrastructure/
│   ├── terraform/, docker/, k8s/
│   └── nginx/
├── monitoring/
│   ├── prometheus/, grafana/, wazuh/
├── scripts/
└── tests/
    ├── unit/, integration/, e2e/
    └── conftest.py
```

**✅ Verification**:
```powershell
ruff check aibe/          # should exit 0
mypy aibe/ --config-file mypy.ini  # should exit 0
python scripts/validate_env.py     # should report missing keys
docker compose config              # should validate without errors
```

---

### Phase 1 — Core Infrastructure Libraries
**Goal**: All shared backbone services that every agent depends on.

> [!IMPORTANT]
> Build order matters. Config → Types → Exceptions → Logging must come first because everything imports from them. DB layer next (agents need persistence). Then bus/memory/router/browser/vault/VM in any order.

#### 1.1 Foundation (no external deps)

##### [NEW] `aibe/core/config.py`
`Settings(BaseSettings)` composing all sub-settings via `env_nested_delimiter="__"`:
- `DatabaseSettings`, `RedisSettings`, `NATSSettings`, `VaultSettings`, `OpenRouterSettings`, `OpenVikingSettings`, `LightpandaSettings`, `CelerySettings`, `ModalSettings`, `WandBSettings`
- Global singleton via `@lru_cache`

##### [NEW] `aibe/core/types.py`
All enums and type aliases:
- `AgentTier(0-9)`, `AgentStatus`, `TaskPriority`, `TaskStatus`
- `MeetingType` (8 values), `ModelTaskType` (9 values), `SecuritySeverity`
- Type aliases: `AgentId`, `TaskId`, `TraceId`, `Namespace`

##### [NEW] `aibe/core/exceptions.py`
Exception hierarchy: `AIBEError` → `BusError`, `MemoryError`, `RouterError`, `BrowserError`, `VaultError`, `VMError`, `AgentError`, `SecurityError`, `BudgetExceededError`

##### [NEW] `aibe/core/logging.py`
structlog JSON logging with bound context (`agent_id`, `task_id`, `trace_id`). Factory function `get_logger(name)`.

#### 1.2 Database Layer (`aibe/core/db/`)

##### [NEW] `postgres.py` — AsyncPG pool + SQLAlchemy async engine/session factory
##### [NEW] `redis.py` — aioredis client with connection pool
##### [NEW] `clickhouse.py` — ClickHouse analytics client (insert events, query aggregations)
##### [NEW] `models.py` — SQLAlchemy ORM models:
- `Agent`, `Task`, `Meeting`, `SecurityScan`, `SecurityFinding`, `Incident`
- `MLExperiment`, `MLModel`, `EvolutionProposal`, `Tool`
- `Contractor`, `FinancialTransaction`, `AuditLog`
##### [NEW] `migrations/env.py` + initial migration

#### 1.3 Message Bus (`aibe/core/message_bus/`)

##### [NEW] `client.py` — `NATSBus`: connect, publish, subscribe, request-reply, auto-reconnect, graceful shutdown
##### [NEW] `models.py` — All Pydantic v2 message types: `TaskAssignMessage`, `SecurityReportMessage`, `ContractorRequestMessage`, `MLProposalMessage`, `SalesHandoffMessage`, `DeploymentGateMessage`, `EscalationMessage`, `MeetingRequestMessage`
##### [NEW] `signing.py` — HMAC-SHA256 sign/verify on every message
##### [NEW] `streams.py` — JetStream stream/consumer/subject configurations
##### [NEW] `middleware.py` — Logging, metrics emission, dead-letter handler
##### [NEW] `replay.py` — Message replay for agent recovery after restart

#### 1.4 Memory System (`aibe/core/memory/`)

##### [NEW] `client.py` — `OpenVikingClient`: store, recall, semantic_search, watch, batch_write
##### [NEW] `namespaces.py` — Full namespace map (`/business/*`, `/agents/{id}/*`, `/meetings/*`, `/research/*`, `/codebase/*`, `/security/*`, `/ml/*`, `/sales/*`, `/contractor/*`, `/marketing/*`, `/social/*`, `/errors/*`, `/evolution/*`, `/tools/*`, `/procurement/*`, `/audit/*`)
##### [NEW] `models.py` — Memory record Pydantic models: `BusinessStateMemory`, `AgentEpisodicMemory`, `MeetingTranscript`, `SecurityVulnerabilityRecord`, `MLModelRecord`, `SalesLeadRecord`, `ContractorEngagementRecord`
##### [NEW] `wal.py` — Write-ahead logging for crash recovery

#### 1.5 Model Router (`aibe/core/router/`)

##### [NEW] `router.py` — `ModelRouter.route_and_call()`: takes `ModelTaskType` + prompt + optional agent context → selects model from routing table → calls OpenRouter API → validates structured output → retries on failure → logs cost
##### [NEW] `routing_table.py` — Loads from `config/routing_table.yaml`. All 9 task types with primary/fallback model chains and per-1K-token cost rates
##### [NEW] `fallback.py` — `FallbackChain` with circuit breaker pattern (track failures, open after N, half-open probe, close on success)
##### [NEW] `metrics.py` — Cost/token/latency tracking → ClickHouse + OpenViking `/audit/cost_log`
##### [NEW] `budget.py` — `BudgetEnforcer`: Redis atomic counters per agent per day. At 80% → downgrade model tier. At 100% → suspend agent + escalate to Oracle.

#### 1.6 Browser Layer (`aibe/core/browser/`)

##### [NEW] `pool.py` — `LightpandaPool`: connection pool with acquire/release, health checks, configurable size
##### [NEW] `client.py` — `BrowserClient`: navigate, extract_text, extract_structured, screenshot, execute_js, wait_for_selector
##### [NEW] `stealth.py` — User-agent rotation, viewport randomization, fingerprint masking
##### [NEW] `cache.py` — Redis-backed response caching with TTL

#### 1.7 Secret Vault (`aibe/core/secret_vault/`)

##### [NEW] `client.py` — `VaultClient` wrapping hvac: get_secret, set_secret, rotate_secret, list_secrets, auto token renewal
##### [NEW] `paths.py` — Path constants organized by agent/service
##### [NEW] `transit.py` — Vault Transit encrypt/decrypt for sensitive data at rest

#### 1.8 VM Manager (`aibe/core/vm_manager/`)

##### [NEW] `manager.py` — `VMManager`: create_sandbox, execute_in_sandbox, destroy_sandbox (Docker SDK)
##### [NEW] `templates.py` — VM templates: `python-dev`, `node-dev`, `security-tools` (pre-installed Semgrep, SQLMap, Nuclei, ZAP)
##### [NEW] `sandbox.py` — Sandboxed execution with CPU/memory/network limits, timeout enforcement

#### 1.9 Cost Tracker (`aibe/core/cost_tracker/`)

##### [NEW] `tracker.py` — Real-time cost aggregation per agent, per model, per task type (Redis + ClickHouse)
##### [NEW] `reporter.py` — Daily/weekly cost reports, budget projections, alerts

#### 1.10 Tool Registry (`aibe/core/tools/`)

##### [NEW] `registry.py` — `ToolRegistry`: register, get, list, invoke, hot-reload from config
##### [NEW] `base_tool.py` — `BaseTool` ABC: name, description, parameters schema, execute
##### [NEW] `builtins/` — `web_search.py`, `code_executor.py`, `file_manager.py`, `http_client.py`, `calculator.py`, `screenshot.py`

**✅ Verification**:
```powershell
pytest tests/unit/core/ -x -q --cov=aibe/core --cov-report=term-missing
# Target: >90% coverage
mypy aibe/core/ --config-file mypy.ini --strict  # exit 0
ruff check aibe/core/                              # exit 0
```

Unit tests for Phase 1 (at minimum):
- `test_config.py` — settings load from env, nested delimiter works, defaults applied
- `test_types.py` — enum values, serialization
- `test_message_bus.py` — publish/subscribe round-trip (mock NATS), message signing
- `test_memory_client.py` — store/recall/search (mock OpenViking)
- `test_model_router.py` — routing table lookup, budget enforcement, fallback chain
- `test_budget_enforcer.py` — 80% downgrade, 100% suspend
- `test_task_validator.py` — valid/invalid task validation

---

### Phase 2 — Base Agent Framework
**Goal**: Abstract agent infrastructure that all 35 agents inherit.

#### 2.1 Agent Base (`aibe/agents/base/`)

##### [NEW] `agent.py` — `BaseAgent(ABC)` with full lifecycle:
- `start()`, `stop()`, `task_loop()`, `execute_task()`, `think()` (LLM call via router)
- `remember()`, `recall()` (OpenViking I/O)
- `use_browser()`, `run_on_vm()` (delegate to core clients)
- `assign_task()`, `escalate()`, `request_contractor()`
- Abstract: `get_system_prompt()`, `on_task_receive()`
- Heartbeat publishing every 30s via NATS

##### [NEW] `context.py` — `AgentContext` dataclass bundling all injected deps (bus, memory, router, browser, vault, vm, registry, db). Factory `create_agent_context()`.

##### [NEW] `lifecycle.py` — State machine: `INITIALIZING → READY → RUNNING → PAUSED → STOPPED → ERROR`. Valid transitions enforced.

##### [NEW] `supervisor.py` — Heartbeat monitor, auto-restart (max 5 in 60s → DEGRADED mode + Oracle escalation), status event publishing.

##### [NEW] `prompts.py` — Jinja2-based `SystemPromptBuilder`: loads agent-specific prompt template, injects dynamic business state from OpenViking, recent decisions, current KPIs.

##### [NEW] `mixins.py` — `BrowserMixin`, `VMMixin`, `AnalyticsMixin`, `SecurityMixin` for optional capabilities.

#### 2.2 Task Delegation (`aibe/agents/delegation/`)

##### [NEW] `task_builder.py` — `TaskBuilder`: pulls OpenViking context (business state, agent history, relevant decisions), classifies for model routing, builds rich task payload.

##### [NEW] `task_validator.py` — `TaskValidator`: quality checks — goal specificity, success criteria present, output schema defined, escalation path set, deliverable write targets, model routing hint valid.

##### [NEW] `task_router.py` — Routes tasks to best agent by capability matrix × current load × availability.

##### [NEW] `models.py` — `Task`, `SubTask`, `TaskResult`, `EscalationRequest`, `ValidationResult` Pydantic models.

#### 2.3 Meeting Engine (`aibe/agents/meetings/`)

##### [NEW] `engine.py` — `MeetingEngine`:
- `convene()` — assemble participants, build briefings
- `build_briefing()` — per-participant context from OpenViking
- `request_contribution()` — prompt each agent for input
- `detect_disagreement()` — compare positions, score divergence
- `run_debate_protocol()` — structured rebuttal rounds
- `synthesize_consensus()` — merge positions
- `request_final_ruling()` — Oracle tiebreaker
- `extract_action_items()` — parse minutes into tasks

##### [NEW] `types.py` — 8 meeting type configs: `STRATEGY_SUMMIT`, `SPRINT_PLANNING`, `SECURITY_REVIEW`, `ML_ROADMAP`, `SALES_PIPELINE_REVIEW`, `INCIDENT_POSTMORTEM`, `EVOLUTION_REVIEW`, `STRATEGY_SUMMIT_EMERGENCY`

##### [NEW] `protocol.py` — Contribution round, disagreement detection, facilitator ruling, consensus scoring

##### [NEW] `briefing.py` — Pre-meeting context generator per participant

##### [NEW] `minutes.py` — Auto-generated minutes + action item extraction

#### 2.4 Agent Registry

##### [NEW] `aibe/agents/registry.py` — Auto-discovery of agents, capability matrix, status tracking, lookup by id/tier/capability.

**✅ Verification**:
```powershell
pytest tests/unit/agents/ -x -q --cov=aibe/agents --cov-report=term-missing
# Target: >85% coverage on aibe/agents/base/
mypy aibe/agents/ --config-file mypy.ini --strict
```

Key tests:
- `test_base_agent.py` — lifecycle transitions, heartbeat, task_loop
- `test_delegation.py` — task building, validation, routing
- `test_meetings.py` — convene flow, disagreement detection, minutes

---

### Phase 3 — All 35 Agent Implementations
**Goal**: Every agent fully implemented. Build in tier order (dependencies flow downward).

> [!IMPORTANT]
> **Build order**: Tier 0 first (Oracle's decisions feed everything). Then Tier 5 (Ledger's budget enforcement is needed by all). Then remaining tiers can be built in parallel.

Each agent: inherits `BaseAgent`, implements `get_system_prompt()` and `on_task_receive()`, defines scheduled/autonomous loops.

#### 3.1 Tier 0 — Executive (`aibe/agents/executive/`)
- `oracle.py` — BUSINESS_DISCOVERY_LOOP, KPI_MONITOR_LOOP (60s), PIVOT_DETECTION_LOOP (daily), COST_MONITOR_LOOP
- `minerva.py` — Business model canvas, OKR management, idea debate chamber

#### 3.2 Tier 5 — Finance & Operations (`aibe/agents/finance/`) *(moved up — budget enforcement needed early)*
- `ledger.py` — Revenue tracking (Stripe webhooks), expense tracking, budget approval, daily P&L, enforcement (80% downgrade / 100% suspend)
- `atlas.py` — API health monitor (6h), uptime monitor (5min), license renewal tracker, compliance checker (monthly)
- `procurator.py` — Full contractor workflow: validate justification → check AI capability → budget review → human approval gate → sourcing → contract management

#### 3.3 Tier 1 — Research (`aibe/agents/research/`)
- `scout.py` — 5-source intelligence pipeline (Reddit, Product Hunt, Google Trends, Keyword Intelligence, Indie Hackers) via Lightpanda + Exa Search
- `vega.py` — Competitor deep-dive: pricing, features, reviews, ads, SEO, tech stack. Weekly re-scrapes
- `pulse.py` — Hypothesis validation with confidence scoring + evidence

#### 3.4 Tier 2 — Product Development (`aibe/agents/product/`)
- `forge.py` — Architecture design, sprint planning (3-day sprints), tech debt monitor
- `ember.py` — Frontend component builder. VM execution + git commit
- `flint.py` — Backend API builder. Tests before completion
- `cinder.py` — Integration specialist. Terraform on VM
- `patch_agent.py` — Bug monitor (Sentry, 5min loop), reproduce + fix + verify
- `deploy_agent.py` — Staging/production deploy, rollback, health checks

#### 3.5 Tier 3 — Marketing (`aibe/agents/marketing/`)
- `helix.py` — Channel strategy, weekly performance review
- `quill.py` — Content calendar, landing page copy, blog posts
- `lumen.py` — Keyword research, on-page audit, rank tracker
- `volt.py` — Campaign launch, optimization loop (6h), hard budget caps
- `prism.py` — Drip sequences, broadcasts, A/B testing, list hygiene

#### 3.6 Tier 4 — Social Media (`aibe/agents/social/`)
- `nova.py` — Content calendar (Monday), brand voice check, performance review
- `spark.py` — Twitter threads, single tweets, trending replies
- `bloom.py` — Instagram posts, TikTok scripts (DALL-E 3, Runway, ElevenLabs)
- `grove.py` — LinkedIn posts/articles, competitor LinkedIn monitoring
- `echo.py` — Monitor all platforms (15min), classify → respond/escalate

#### 3.7 Tier 6 — Evolution (`aibe/agents/evolution/`)
- `darwin.py` — Analysis loop (48h + triggers), proposals, shadow validation
- `synth.py` — Tool builder (write, test, document, register), agent persona builder

#### 3.8 Tier 7 — AI/ML (`aibe/agents/ai_ml/`)
- `cipher.py` — Opportunity scanner (weekly), proposal generator, ROI tracker
- `tensor.py` — ETL pipelines, feature store, data quality monitor
- `neural.py` — Architecture selection, training (Modal/local), evaluation, staging deploy. W&B tracking
- `optimus.py` — 5 prediction systems: churn, pricing, recommendations, ad audience, email timing
- `automata.py` — Process discovery (weekly), automation builder (Make/Zapier), automation monitor

#### 3.9 Tier 8 — Cybersecurity (`aibe/agents/security/`)
- `sentinel.py` — Security dashboard, remediation tracker, deploy gate (blocks on HIGH+), quarterly reports
- `vault_keeper.py` — Secret rotation (30d external / 7d internal), access audit, leak response
- `auditor.py` — Commit scan pipeline (Semgrep, Bandit, GitLeaks, Grype, Checkov), daily infra scan, LLM false-positive filtering, structured remediation reports
- `penetest.py` — 4 test suites (web, API, infra, business logic), OWASP Top 10, professional reports
- `incident_responder.py` — 24/7 monitor (Wazuh, Cloudflare, Sentry), 4 playbooks

#### 3.10 Tier 9 — Sales (Conditional) (`aibe/agents/sales/`)
- `mercury.py` — Activation engine: score business model → activate/deactivate team. Starts dormant
- `closer.py` — 4-touchpoint outreach sequence, CRM tracking
- `orator.py` — Inbound lead handling, qualification, demo scheduling
- `guardian.py` — Support (7 types), human escalation (8 conditions)
- `escalator.py` — Human handoff package builder, Slack/email notification

#### 3.11 Config
##### [NEW] `aibe/config/agents.yaml` — Per-agent routing profile: default_task_type, allowed_task_types, daily_llm_budget_usd for all 35 agents.

**✅ Verification**:
```powershell
pytest tests/unit/agents/ -x -q --cov=aibe/agents --cov-report=term-missing
# Target: >75% coverage per tier module
# Integration test: Oracle → Forge → Flint → Patch → Deploy pipeline
# Integration test: full meeting lifecycle
```

---

### Phase 4 — API Server & Workers
**Goal**: FastAPI backend + Celery workers serving the UI and real-time events.

#### 4.1 API Server (`aibe/ui/backend/`)

##### [NEW] `main.py` — FastAPI app factory with lifespan (connect/disconnect all clients), CORS, middleware stack
##### [NEW] `deps.py` — Dependency injection: `get_db()`, `get_bus()`, `get_memory()`, `get_registry()`
##### [NEW] `auth.py` — JWT validation, API key auth, RBAC roles (admin/viewer/agent)
##### [NEW] `websocket_server.py` — Full WS server: `build_system_snapshot()` on connect, typed event streaming (agent_*, meeting_*, security_*, sales_*, ml_*, system_*)
##### [NEW] `routes/`
| Route | Endpoints |
|---|---|
| `/api/system` | launch, status, health |
| `/api/agents` | list, detail, status, logs |
| `/api/tasks` | list, create, status |
| `/api/meetings` | list, detail, convene |
| `/api/memory` | search, browse namespaces |
| `/api/security` | scans, findings, gate status |
| `/api/finance` | P&L, costs, contractors |
| `/api/ml` | models, experiments, pipelines |
| `/api/sales` | pipeline, leads, conversations |
| `/api/evolution` | proposals, tools, analysis |

##### [NEW] `schemas/` — Pydantic response models for all endpoints

#### 4.2 Celery Workers (`aibe/workers/`)

##### [NEW] `celery_app.py` — Redis broker/backend, named queues (default, security, ml)
##### [NEW] `tasks/` — agent_tasks, meeting_tasks, security_tasks, ml_tasks, evolution_tasks, finance_tasks, maintenance_tasks
##### [NEW] `schedules.py` — Celery Beat schedule: budget checks (hourly), metric aggregation (hourly), P&L (daily), failure analysis (daily), security audit (daily), cleanup (weekly)

**✅ Verification**:
```powershell
pytest tests/unit/api/ -x -q
# Swagger UI accessible at http://localhost:8000/docs
# WebSocket connect + event delivery tested
# Celery task execution verified
```

---

### Phase 5 — Next.js 15 Frontend (2D Dashboard)
**Goal**: Complete dashboard UI with all 12 screens. Ship the 2D Agent Universe first; 3D is Phase 6 enhancement.

#### 5.1 Scaffold
- Next.js 15 App Router, TypeScript strict, TailwindCSS, shadcn/ui
- Dependencies: React 19, Zustand, React Query, Framer Motion, React Flow, Tremor, Recharts, xterm.js, Socket.IO client

#### 5.2 Layout & Shared
- `SystemStatusBar` (top) — system health, agent count, active tasks, cost today
- `Sidebar` (left nav) — all page links, collapsible
- `NotificationPanel` (slide-in) — real-time alerts and events
- `lib/ws-client.ts` — Typed WebSocket client with reconnect + exponential backoff
- `lib/api-client.ts` — Typed REST client with React Query integration
- Zustand stores: `agent-store`, `meeting-store`, `notification-store`

#### 5.3 Pages

| Page | Route | Key Components |
|---|---|---|
| Command Center | `/` | `AgentUniverse.tsx` (React Flow), `LiveFeed.tsx`, `QuickActions.tsx` |
| Agent Detail | `/agents/[id]` | `AgentDetailPanel.tsx`, `ReasoningStream.tsx`, `MemoryTimeline.tsx`, `VMTerminal.tsx` (xterm.js) |
| War Room | `/meetings` | `LiveMeetingView.tsx`, `DebatePanel.tsx`, `DecisionLedger.tsx` |
| Builder View | `/product` | Codebase map, deployment pipeline, bug tracker |
| Marketing Command | `/marketing` | Campaigns, content calendar, SEO dashboard |
| Social Studio | `/social` | Post preview, engagement feed, trend radar |
| Security Ops | `/security` | `SecurityGate.tsx`, `VulnerabilityBoard.tsx` (Kanban), `ThreatFeed.tsx` |
| Sales & CS | `/sales` | `PipelineKanban.tsx`, `LiveConversations.tsx`, `EscalationQueue.tsx` |
| AI/ML Lab | `/ml` | `ModelRegistry.tsx`, `ExperimentTracker.tsx`, `PipelineHealth.tsx` |
| Evolution Lab | `/evolution` | Proposals timeline, tool registry, Darwin analysis |
| Finance & Ops | `/finance` | `PLDashboard.tsx`, `CostControl.tsx`, `ContractorTracker.tsx` |
| Settings | `/settings` | Routing table editor, budget limits, agent toggles, logs |

#### 5.4 Agent Universe (2D — React Flow)
- Custom `AgentNode` component: pixel avatar, tier color, status badge, activity pulse, task tooltip
- `AnimatedEdge` for message-in-transit visualization
- Team clustering layout with department zones

**✅ Verification**:
```powershell
cd aibe/ui/frontend && npm run build   # zero TS errors
npm run lint                            # clean
# All pages render with mock data
```

---

### Phase 6 — 3D Pixelated Virtual Office
**Goal**: Immersive isometric pixel-art office showing all 35 agents as voxel characters.

**Technology**: React Three Fiber + Three.js + custom pixelation shader

#### 6.1 Core Scene (`components/3d/`)
- `Scene.tsx` — R3F Canvas, isometric camera, OrbitControls, pixelation post-processing
- `OfficeFloor.tsx` — Voxel floor plan via InstancedMesh. Department zones by color (gold=Executive, blue=Research, green=Dev, orange=Marketing, pink=Social, teal=Finance, purple=Evolution, cyan=AI/ML, red=Security, yellow=Sales)
- `AgentCharacter.tsx` — 8×8×16 voxel humanoid per agent. Animation states driven by WS events: idle, walking, coding, meeting, thinking, error, processing
- `Furniture.tsx` — Low-poly desks, chairs, meeting tables, servers, monitors, plants
- `Pathfinding.ts` — A* grid navigation with smooth lerp interpolation
- `MeetingRoom.tsx` — Agents walk to conference room on `meeting_started`, speech bubbles for contributions
- `Minimap.tsx` — HTML overlay with colored dots, click-to-teleport
- `DayNightCycle.tsx` — Light shifts over 24h real clock
- `Effects.tsx` — Pixelation shader (1/4 res, nearest-neighbor upscale), AO, bloom

#### 6.2 State Management
- `stores/virtual-office-store.ts` — camera position, selected agent, follow mode, zoom level
- Backend authoritative state via WS `/ws/virtual-space/state` (every 2s or on change)

#### 6.3 Performance
- InstancedMesh for all repeated geometry
- LOD for distant agents
- Cap 3D scene to 30fps (UI stays 60fps)
- 2D fallback if WebGL unavailable

**✅ Verification**:
```
# 35 agents visible and animated at 60fps
# Pixelation shader active
# Agents respond to WebSocket events
# Meeting walk-to-room flow works
```

---

### Phase 7 — Launch Sequence & Integration
**Goal**: Single-button launch from the UI.

##### [NEW] `aibe/core/orchestrator/launch.py`
`execute_launch_sequence()`:
1. Infrastructure health check (Postgres, Redis, NATS, ClickHouse, Vault)
2. Run DB migrations
3. Initialize JetStream streams
4. Initialize Vault policies
5. Start browser pool
6. Initialize model router + budget enforcer
7. Start security monitoring
8. Start cost tracking
9. Staggered agent startup (10 groups, 3.5 agents each)
10. Read business state from OpenViking
11. If first launch → BUSINESS_DISCOVERY. If resume → RECOVERY_LOOP.

##### [NEW] `aibe/ui/backend/routes/system.py`
- `POST /api/system/launch` — triggers the sequence
- Real-time boot step streaming via WebSocket

##### Frontend — Launch button on Command Center home screen

**✅ Verification**:
```
# POST /api/system/launch → 35 agents register, heartbeats flowing
# UI shows real-time boot progress
# Business discovery starts (or resumes)
```

---

### Phase 8 — Tests & Coverage
**Goal**: Comprehensive test suite.

```
tests/
├── conftest.py              # mock_bus, mock_memory, mock_router, testcontainers, factories
├── unit/
│   ├── core/                # >90% coverage
│   ├── agents/              # >75% coverage (one test file per agent)
│   ├── security/            # >85% coverage
│   └── api/
├── integration/
│   ├── test_agent_communication.py
│   ├── test_openviking_client.py
│   ├── test_security_gate.py
│   ├── test_sales_activation.py
│   └── test_ml_pipeline.py
└── e2e/
    ├── test_launch_sequence.py
    ├── test_business_discovery.py
    └── test_security_incident.py
```

Frontend: Vitest + React Testing Library for components; Playwright for critical flows.

**✅ Verification**:
```powershell
pytest tests/ -x -q --cov=aibe --cov-report=term-missing
# Core ≥90%, Security ≥85%, Agents ≥75%
```

---

### Phase 9 — Monitoring, Infra Configs & Hardening
**Goal**: Production-ready monitoring and resilience.

#### Monitoring configs
- `monitoring/prometheus/prometheus.yml` — Scrape configs for all services, alert rules
- `monitoring/grafana/dashboards/` — 4 dashboards (Agent Overview, Infrastructure, Business KPIs, Security)
- `monitoring/wazuh/ossec.conf` — SIEM agent config

#### Infrastructure configs
- `infrastructure/nats/nats-server.conf` — JetStream, file storage 10GB, auth
- `infrastructure/vault/config.hcl` + `policies/` — agent-policy, admin-policy
- `infrastructure/nginx/nginx.conf` — Reverse proxy, WebSocket upgrade, gzip, rate limit, SSL

#### Resilience
- Agent supervisor: max 5 restarts in 60s → DEGRADED + escalation
- Message bus: JetStream persistence, unprocessed message replay on restart
- OpenViking: WAL on all writes, idempotent writes
- Degraded mode: if >30% agents offline → pause non-critical tasks
- Security gate fail-safe: if Auditor offline → deployments BLOCKED

**✅ Verification**:
```powershell
docker compose up -d  # all containers healthy within 60s
# Prometheus scraping targets active
# Grafana dashboards loading
# Kill agent → supervisor restarts within 10s, no lost messages
```

---

## Verification Matrix (Definition of Done)

| # | Acceptance Test | Pass Criteria | Phase |
|---|---|---|---|
| 1 | One-command setup | `setup.ps1` → deps installed, .env created, pre-commit ready | 0 |
| 2 | Docker up | `docker compose up -d` → all containers healthy ≤60s | 0, 9 |
| 3 | Launch sequence | `POST /api/system/launch` → 35 agents register, heartbeats flowing | 7 |
| 4 | Agent communication | Oracle assigns Scout → Scout produces market scan → stored in OpenViking | 1, 3 |
| 5 | Meeting flow | Strategy Summit → 5 agents → disagreement → debate → ruling → minutes + action items | 2, 3 |
| 6 | Task delegation | TaskBuilder → rich context → TaskValidator passes → agent receives and executes | 2 |
| 7 | Security gate | Auditor finds HIGH → Deploy blocked → Patch fixes → Auditor verifies → gate cleared | 3 |
| 8 | Budget enforcement | Agent at 80% → router downgrades model → at 100% → suspended | 1 |
| 9 | Cost tracking | Every LLM call logged (agent, model, tokens, cost) → visible in Finance UI | 1, 5 |
| 10 | Sales activation | Mercury scores business model → activates/deactivates sales team | 3 |
| 11 | ML pipeline | Cipher proposes → Tensor builds features → Neural trains → Optimus deploys | 3 |
| 12 | Contractor flow | Agent requests → Procurator validates → Ledger approves → engaged | 3 |
| 13 | Evolution cycle | Darwin detects pattern → proposes tool → Synth builds → registered | 3 |
| 14 | Incident response | Incident detected → playbook executes → Oracle notified → tracked | 3 |
| 15 | All UI pages | 12 pages render with real-time WebSocket data | 5 |
| 16 | 3D Virtual Office | 35 pixel agents, walking/coding/meeting animations, 60fps, pixelation shader | 6 |
| 17 | Agent Universe | React Flow graph with all agents, status indicators, animated edges | 5 |
| 18 | Type safety | `mypy aibe/ --strict` exits 0; `tsc --noEmit` exits 0 | All |
| 19 | Test coverage | ≥90% core, ≥85% security, ≥75% agents | 8 |
| 20 | Resilience | Kill agent → supervisor restarts ≤10s, no lost messages | 9 |
| 21 | CI pipeline | Push → lint + typecheck + tests pass | 0 |

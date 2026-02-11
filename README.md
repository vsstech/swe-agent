# SWE Agent

An **agentic software engineering assistant** that analyzes Python repositories, evaluates code quality and test coverage, generates missing unit tests, and recommends dependency updates — all through a **bounded, auditable agent loop**.

This project is designed as a **portfolio-grade system** that demonstrates real-world agentic design, CI/CD integration, and safe LLM usage.

---

## High-Level Capabilities

- 🔍 Static analysis (linting)
- 🧪 Test execution & coverage analysis
- 🧠 Agentic planning (LLM decides *what* to do, not *how*)
- ✍️ Automated unit test generation (safe, constrained)
- 📦 Third-party dependency checks
- 🔁 Feedback-driven iteration toward a goal
- 🤖 Reusable GitHub Action for CI pipelines

---

## Architecture Overview

```
┌────────────────────────────────────────┐
│        Target Repository (User)        │
│                                        │
│  ┌──────────────────────────────────┐  │
│  │ GitHub Action Workflow            │  │
│  │ .github/workflows/swe-agent.yml  │  │
│  └──────────────┬───────────────────┘  │
│                 ↓                      │
│  ┌──────────────────────────────────┐  │
│  │ swe-agent-action (Composite)     │  │
│  │ - action.yml                     │  │
│  │ - installs swe-agent             │  │
│  │ - runs CLI                       │  │
│  └──────────────┬───────────────────┘  │
│                 ↓                      │
│  ┌──────────────────────────────────┐  │
│  │ swe-agent (Python Library)       │  │
│  │                                  │  │
│  │  ┌──────────────┐                │  │
│  │  │ Agent Loop   │                │  │
│  │  │ (Plan→Act→   │                │  │
│  │  │  Observe)   │                │  │
│  │  └──────┬───────┘                │  │
│  │         ↓                        │  │
│  │  ┌────────────────────────────┐ │  │
│  │  │ Deterministic Tools         │ │  │
│  │  │ - Lint                      │ │  │
│  │  │ - Pytest + Coverage         │ │  │
│  │  │ - Coverage Parser           │ │  │
│  │  │ - Test Generator            │ │  │
│  │  │ - Dependency Checker        │ │  │
│  │  └────────────────────────────┘ │  │
│  └──────────────────────────────────┘  │
└────────────────────────────────────────┘
```

**Key design rule:**
> The LLM never executes code. It only selects the next action.

---

## Step-by-Step Design (Step 1 → Step 10)

---

## Step 1: Define the Goal

The agent is always driven by a **clear, explicit goal**.

Example:
```
Improve test coverage to at least 80% without changing production code
```

This goal is passed to the agent and used by the planner to decide actions.

---

## Step 2: Repository Analysis Inputs

The agent receives:
- Repository path
- Reports/output directory
- Goal text

No assumptions are made about project structure beyond standard Python tooling.

---

## Step 3: Deterministic Tooling Layer

The existing analysis pipeline is preserved as **tools**:

- `run_ruff()` – linting
- `run_pytest_coverage()` – test execution
- `parse_coverage_xml()` – coverage parsing
- `suggest_tests_for_file()` – test gap analysis
- `generate_test_file()` – controlled test generation

These tools:
- Are deterministic
- Can be tested independently
- Never call the LLM

---

## Step 4: Agent State (Memory)

The agent maintains explicit state:

- Goal
- Observations (tool outputs)
- Actions taken
- Coverage metrics
- Whether tests were generated

This makes every run:
- Auditable
- Replayable
- Debuggable

---

## Step 5: LLM Planner (Decision Maker)

The planner:
- Receives the goal and observations
- Chooses **one action** from a fixed set

Allowed actions include:
- `run_lint`
- `run_tests`
- `analyze_coverage`
- `generate_tests`
- `create_pr`
- `stop`

The planner **cannot** run tools or modify code directly.

---

## Step 6: Tool Executor (Safety Boundary)

A strict executor layer:
- Maps actions → tools
- Enforces safety rules
- Collects observations

This separation ensures:
- LLM mistakes do not cause damage
- Business logic lives in code, not prompts

---

## Step 7: Agent Loop (Plan → Act → Observe)

The core agent loop:

1. Plan next action
2. Execute one tool
3. Observe results
4. Update state
5. Check stopping conditions

The loop is:
- Bounded by max steps
- Goal-aware
- Feedback-driven

---

## Step 8: Stopping Conditions & Safety

The agent stops when:
- Coverage goal is met
- No useful actions remain
- Maximum steps reached

Hard constraints:
- Never modify production code
- Never auto-merge PRs
- Never exceed action budget

---

## Step 9: CLI Interface

The agent is exposed as a CLI:

```
swe-agent --repo-path . --goal "Improve test coverage to 80%"
```

This allows:
- Local execution
- CI integration
- Reuse by GitHub Actions

---

## Step 10: Reusable GitHub Action

A separate repository (`swe-agent-action`) wraps the CLI as a **composite GitHub Action**.

Users enable the agent by adding:

```
- uses: yourname/swe-agent-action@v1
  with:
    goal: "Improve test coverage to 80%"
```

This mirrors how real-world developer tools are adopted.

---

## Why This Design Is Agentic (Not Just Automation)

| Capability | Supported |
|----------|-----------|
Goal-driven behavior | ✅ |
Planning & decision-making | ✅ |
Tool selection | ✅ |
Feedback loop | ✅ |
Explicit memory | ✅ |
Safety boundaries | ✅ |

---

## Why This Matters 

This project demonstrates:
- Agentic system design
- Safe LLM integration
- CI/CD engineering
- Tool abstraction
- Enterprise-ready constraints

**This is not a demo agent — it is a system.**

---

## Future Enhancements

- PR comments with coverage diffs
- Multi-agent specialization (tests, deps, lint)
- Persistent memory across runs
- Policy-driven governance
- Human-in-the-loop approvals

---

## Summary

SWE Agent shows how to build **real, controlled autonomy** for software engineering tasks — balancing LLM intelligence with deterministic, auditable systems.


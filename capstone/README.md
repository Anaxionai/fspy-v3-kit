# Your personal capstone

In the last six weeks of the course you build your own product. You plan it in week 23, and your mentor approves the plan. The portal then turns it into your own tasks for weeks 24 to 28. You reuse code from your projects, and in the second half a coding agent works with you.

## The six weeks

| Week | Module | What happens | Gate |
|---|---|---|---|
| 23 | CP1: plan and design | Learn cards, then your plan, one part per task. A plan review with your mentor. | |
| 24 and 25 | CP2: build the core | Your generated tasks for milestone M1. Chat AI may help; coding agents may not. | |
| 26 and 27 | CP3: extend it with a coding agent | Your generated tasks for milestone M2. A coding agent helps in the tasks that say so. | G8 at the end of week 27 |
| 28 | CP4: ship it and defend it | Your generated tasks for M3: a load test and a real deploy. Your CV and two mock interviews. | G9, the final defence |

## How it works, step by step

### 1. Choose a brief or pitch your own idea

Read the four briefs and pick one:

| Brief | The product |
|---|---|
| [ClinicDesk](briefs/clinicdesk.md) | Appointments, a live token queue and fees for a neighbourhood clinic |
| [Marketplace](briefs/marketplace.md) | An online market where local makers sell to buyers in their city |
| [Course platform](briefs/course-platform.md) | Video courses, payments and quizzes for a coaching institute |
| [Shared expenses](briefs/shared-expenses.md) | Shared bills and balances for flatmates and friends on a trip |

You may pitch your own idea instead, if it passes these four tests:

- It fits five weeks at about 20 hours a week, with 10 to 15 stories.
- It uses all six required parts (below).
- It needs no idea the course has not taught, or at most three that a learn card can teach in an hour each.
- It needs no real personal data, no real money and no data copied from a website that does not allow it.

Your mentor tells you early if a pitch is too big.

### 2. Fill in your plan

Copy [`plan-template/PLAN.md`](plan-template/PLAN.md) to `capstone/PLAN.md` in your task folder. Each CP1 task fills one part:

| Part of `PLAN.md` | CP1 task |
|---|---|
| `## Product` and the first draft of `## Required parts` | Choose a brief or pitch your own idea |
| `## Users and stories`: 10 to 15 stories with Given, When, Then criteria | Write 10–15 user stories with acceptance criteria |
| `## Data model`: an ERD in Mermaid | Draw the ERD |
| `## API contract`, with the full contract in `capstone/openapi.yaml` | Write the API contract in OpenAPI |
| `## Architecture`, with `### Context` and `### Containers` | Draw C4 context and container diagrams |
| `## Decisions`: three records in `capstone/docs/adr/0001-<short-name>.md` to `0003` | Write three decision records |
| `## Cost`: AWS and one other cloud, a month | Estimate the monthly cost on two clouds |
| `## Milestones` and the finished `## Required parts` | Split the work into milestones and submit the plan |

Start your contract from [`plan-template/openapi.yaml`](plan-template/openapi.yaml). Keep every heading of `PLAN.md` exactly as it is: the tool that writes your tasks finds each part by its heading.

Your plan has three milestones, one for each module. Each has a budget of hours, which leaves room for the module's course tasks and its wrap-up:

| Milestone | Weeks | Budget | What goes in it |
|---|---|---|---|
| M1 Core | 24 and 25 | about 34 hours | Sign-in and roles, the Must stories, your payments-or-uploads part, and tests for the core flows |
| M2 Extend | 26 and 27 | about 28 hours | The features you build with a coding agent, your live-updates-or-AI part, Kubernetes, the pipeline with infrastructure as code, and observability |
| M3 Ship | 28 | about 10 hours | The load test, the budget alarm and the real deploy, and the cost report |

### 3. Your mentor approves the plan

In week 23 you have a plan review session with your mentor. Find it on Calendar and answer Going. You walk through your plan in five minutes, and your mentor checks five things:

- the scope fits five weeks;
- every required part is used by a feature;
- the ERD and the API contract agree;
- the cost estimate is reasonable;
- nothing in the plan needs an idea the course has not taught, without a plan for learning it.

Write every note in `capstone/PLAN-REVIEW.md` and change the plan to match. Your mentor then approves the plan, or sends it back with notes and a date for the next review.

### 4. Your tasks are generated

After approval, AxPlanner (the tool that writes capstone tasks) reads the approved `capstone/PLAN.md` in the folder of your plan-review task. Keep the plan up to date there. AxPlanner writes tasks of 1 to 3 hours for CP2, CP3 and CP4, and your mentor checks them before you see them.

- Your tasks appear on your board after the course tasks of each module, marked "Assigned to you".
- Each one has a brief and a "What AxReview checks" list, like every other task, and AxReview grades it the same way.
- If a task needs an idea the course never taught, a learn card comes before it.
- Your product lives in a `capstone/` folder inside each task folder. Each task tells you to copy it forward from the task before. Your first generated task copies it from the folder of your plan-review task.

For now, a staff member creates your tasks with a script. The portal sends you one notification and one email for each task: about 30 at once. Your mentor tells you before it happens.

### 5. Re-planning

Plans change. If a feature is too big or a part does not work, talk to your mentor, usually at your Friday demo. If you agree a change:

- you update `capstone/PLAN.md` in your current task folder;
- only tasks you have not started are swapped for new ones;
- tasks you have started stay on your record, with your work and their reviews;
- a change cannot drop a required part, and each milestone must still fit its hours.

## The six required parts

Every capstone has all six. For the two "or" parts, you choose one option.

| Required part | What it means in your product | Where you learnt it |
|---|---|---|
| Sign-in and roles | Sign-up and sign-in, at least two roles, and checks that a user sees only what they own | RailSeat accounts (P5) |
| Payments or uploads | Payments through MockPay with signed webhooks and a ledger, or files uploaded straight to object storage with presigned URLs | RailSeat payments (P6) or ReelPipe (P8) |
| Live updates or a small AI answer feature | Updates that appear without a refresh, through WebSockets and Redis pub/sub, or answers to questions about your own documents, with citations | TiffinTrack (P9) or Ask RailSeat (P10) |
| Tests and a pipeline with infrastructure as code | Unit, API and end-to-end tests in a GitHub Actions pipeline, and OpenTofu that creates at least one resource on the cloud lab | Shortly ships (P11) |
| Containers and Kubernetes | A Compose stack on your laptop, and a Helm chart that runs the product on k3d | Shortly (P7) and TiffinTrack on Kubernetes (P12) |
| Observability, a real deploy and a cost report | Traces, metrics, a dashboard and one alert. One deploy to AWS behind a $5 budget alarm, torn down the same day. A report of the real cost. | TiffinTrack on Kubernetes (P12) and Shortly live (P13) |

Reuse your own code from these projects: it is your parts bin. Copying another student's code is not reuse.

## The AI rules

| Tool | When | What to record |
|---|---|---|
| AxTutor | Every week | Nothing. It teaches; it never writes your code. |
| Chat AI, such as ChatGPT, Claude or Gemini | CP1 and CP2 (weeks 23 to 25), and later for questions | Each use in `AI_LOG.md` in the task folder: what you asked, what it said, what you kept, what you changed and what was wrong |
| A coding agent (an AI tool that edits your files and runs commands), the one your centre provides | CP3 and CP4 only (weeks 26 to 28), and only in tasks that say so | Each change in `AGENT_LOG.md` in the task folder, in six parts |

Each `AGENT_LOG.md` entry has the six parts the CP3 card "Working with a coding agent" teaches:

```
## 2027-06-29 · Bill photos with the agent
Spec:     docs/specs/receipts.md, change 2 of 3: the presigned upload route
Plan:     the agent's plan in two lines, and what I changed in it
Diff:     the files it changed (from git diff --stat)
Kept:     the route and its membership check
Rejected: a new package it added for dates; I used the standard library
Tested:   uv run pytest -q, 41 passed; one upload by hand on Floci
```

Three rules have no exceptions:

- No coding agent before CP3.
- No AI for gate answers or for your defence answers.
- You must be able to explain every line of your product. The G9 defence may ask about any line.

## Where your files go

Inside `capstone/`, copied forward from task to task:

- `PLAN.md`, `PLAN-REVIEW.md`, `openapi.yaml` and `docs/adr/0001-<short-name>.md` onwards;
- `api/`, `web/`, `compose.yaml`, `infra/`, `helm/`, `ops/` and `docs/`.

In the task folder itself, outside `capstone/`:

- `evidence.md`: pasted command output, such as test runs;
- `AI_LOG.md` and `AGENT_LOG.md`;
- in CP4: `cv-lines.md`, `mock-technical.md` and `mock-system-design.md`.

AxReview reads only the task's own folder, so copy `capstone/` forward every time a task tells you to.

## Every week

- **Demos:** each week from week 24 to week 28 you show one story working end to end at a demo session with your mentor. It is on a Friday, or earlier in a gate week. Find it on Calendar and answer Going.
- **Gates:** G8 at the end of week 27 checks your build and your agent work. G9 in week 28 is the final defence: you walk through your deploy and explain any line of your code.
- **Help:** each task's "Stuck?" lines, AxTutor, and your mentor's office hours.

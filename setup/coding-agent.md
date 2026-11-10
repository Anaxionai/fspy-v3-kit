# Coding agents: set one up and use it safely (CP3 and CP4)

A **coding agent** is an AI tool that reads your project, edits files and runs commands for you.
The course uses one only in the capstone's last two modules, CP3 and CP4. Before that, chat AI may help you, but you write the code.
Your mentor tells you which agent your centre uses. This page covers three, checked on 10 November 2026.

## Which agent, and what it costs

| Agent | Where it runs | Cost for you | Good to know |
|---|---|---|---|
| **GitHub Copilot, agent mode** | Inside VS Code | Free with **Copilot Free**, which limits agent use each month. Verified students get **Copilot Student**, also free, through GitHub Education. | The easiest start, because it is built into VS Code. |
| **Claude Code** | Git Bash, PowerShell or VS Code | Needs a paid Claude plan (Pro or higher) or an Anthropic API account. The free Claude plan does not include it. | Use it when your centre gives you a seat. |
| **Gemini CLI** | Git Bash or PowerShell | Its free sign-in with a personal Google account ended on 18 June 2026. It still works with a Gemini API key, within that key's limits. | Google moved free personal use to its new Antigravity CLI. Use either only if your mentor names it. |

### Copilot for students

1. Sign in to GitHub and open https://github.com/settings/education/benefits.
2. Apply as a student. GitHub asks for proof that you study, such as your college email address or your student identity card.
3. When GitHub approves you, Copilot Student appears in your account. GitHub checks every month that you are still a student.

Until you are approved, Copilot Free works, with a smaller monthly allowance.

## Install and sign in

### GitHub Copilot in VS Code

1. In VS Code, select the **Accounts** icon (bottom left) and sign in with GitHub.
2. Open the Chat view with Ctrl+Alt+I. VS Code sets up Copilot when you first open it.
3. In the Chat view, choose the **Agent** mode.

Check it: ask "Which files are in this folder?" The agent lists them.

### Claude Code

In PowerShell:

```powershell
irm https://claude.ai/install.ps1 | iex
```

Or, in Git Bash, with the Node.js you installed in week 2: `npm install -g @anthropic-ai/claude-code`.
Then open a new terminal in your project folder and start it with `claude`. It asks you to sign in the first time.
Claude Code runs its commands in Git Bash when Git for Windows is installed, as it is on your laptop.

Check it: `claude --version` prints a version number.

### Gemini CLI

In Git Bash: `npm install -g @google/gemini-cli`, then start it with `gemini` in your project folder. To use your Gemini API key from P10, set `GEMINI_API_KEY` before you start it, as `ask-railseat.md` in the kit's `data/railseat` folder shows.

Check it: `gemini --version` prints a version number.

## The safe loop: spec, plan, small diff, review, test

Follow these steps for every change you ask an agent to make.

1. **Commit first.** Start from a clean `git status`, so you can always go back.
2. **Write a spec** in `spec.md`: one change, the test that proves it works and the files the agent may change. Add "no new packages", unless you need one.
3. **Ask for a plan only:** "Read spec.md and reply with a plan. Do not change any files yet."
   - Copilot: use the Plan agent (type `/plan`).
   - Claude Code: switch to plan mode with Shift+Tab, or start it with `claude --permission-mode plan`.
   - Gemini CLI: start it with `gemini --approval-mode plan`.
4. **Check the plan.** It must name the files you expect and a test. Change what is wrong before you approve it.
5. **Let the agent make the change.** Keep each change small enough to read in one sitting.
6. **Read the diff:** run `git diff --stat`, then `git diff`, and read every changed line.
7. **Run the tests yourself:** for example `uv run pytest -q` or `npm test`. Never trust the agent's own report that the tests pass.
8. **Keep or undo.** Commit what you keep. Undo the rest with `git restore .` and delete any new files you do not want.
9. **Log it** in `AGENT_LOG.md` (see below).

## Rules that keep you safe

- **Approve each command.** Keep the agent in its default mode, where it asks before it runs a command or edits a file. Do not switch on any "approve everything" mode, such as Gemini CLI's `yolo` mode.
- **Never give an agent a secret.** Keep keys in `.env`, which Git ignores. Do not paste a password, token or API key into the chat.
- **Check every new package.** Agents sometimes invent package names, and attackers publish look-alike names. Before you accept a new package, find it on pypi.org or npmjs.com under that exact name and check who maintains it.
- **Watch for weaker tests.** If the agent changed a test so that it passes, compare the test with your spec. Restore the real check and reject the change if the behaviour is wrong.
- **Stay in scope.** If the agent changes files outside your spec, reject the change and add "change only these files" to the spec.
- **Mind your data.** On free plans, your prompts and code may be used to train AI models. GitHub Copilot Free lets you switch this off. In your GitHub settings under Copilot, turn off "Allow GitHub to use my data for AI model training".
- **Undoing has limits.** Undo in the editor puts files back, but a command the agent already ran (such as a migration or `rm`) stays done. That is why you commit first and approve each command.

## `AGENT_LOG.md`: one entry for each agent change

Keep `AGENT_LOG.md` in your task folder. Each entry has six parts:

| Part | What you write |
|---|---|
| **Spec** | The change you asked for, or a link to `spec.md` |
| **Plan** | The agent's plan in two or three lines, and what you changed in it |
| **Diff** | The `git diff --stat` output: which files changed, and how many lines |
| **Kept** | The parts you accepted, and why |
| **Rejected** | The parts you undid or asked the agent to redo, and why |
| **Tested** | The test command you ran yourself, and its last lines |

An example entry:

```markdown
## 2026-12-03: add a --top N option to the report command

- **Spec:** spec.md: add `--top N` (default 10) to `paisalens report`; test in tests/test_cli.py; change only cli.py and report.py; no new packages.
- **Plan:** edit cli.py and report.py, add one test. I changed the default from 5 to 10.
- **Diff:** 3 files changed, 24 insertions(+), 4 deletions(-).
- **Kept:** the new option and its test.
- **Rejected:** the agent also renamed `render_report`; outside the spec, so I undid it.
- **Tested:** `uv run pytest -q`: 31 passed in 0.62s (I ran it myself).
```

A log where nothing was ever rejected usually means the diffs were not read. Your mentor asks about your log at each demo.

## Official guides

- Agents in VS Code (Visual Studio Code docs): https://code.visualstudio.com/docs/agents/overview
- Free access with Copilot Student (GitHub Docs): https://docs.github.com/copilot/how-tos/manage-your-account/free-access-with-copilot-student
- Set up Claude Code (Anthropic): https://code.claude.com/docs/en/setup
- Best practices for Claude Code (Anthropic): https://code.claude.com/docs/en/best-practices
- Gemini CLI documentation (Google): https://geminicli.com/docs/

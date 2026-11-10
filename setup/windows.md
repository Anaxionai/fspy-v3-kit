# Set up your Windows laptop

This guide sets up a Windows 11 laptop for the whole course.
Everything runs on Windows, and **Git Bash is your terminal**, inside VS Code.
Do Part 1 in week 1 and Part 2 in week 2. After each step, run its check before you go on.

The versions the course uses are in [`VERSIONS.md`](../VERSIONS.md).

## Before you start

- **Windows 11, version 23H2 or newer.** Press Windows+R, type `winver` and press Enter to see your version. Docker Desktop needs 23H2 or newer.
- **At least 8 GB of memory** and **15 GB of free disk space**.
- **Virtualisation turned on.** Open Task Manager, select Performance, then CPU. It must say `Virtualization: Enabled`. If it says Disabled, ask your mentor to turn on Intel VT-x or AMD SVM in the laptop's BIOS.
- **An administrator account** on the laptop, because the installers change system settings.
- Keep the charger plugged in. If your laptop does not run Windows, ask your mentor for the matching steps.

## Where each tool lives

| Tool | Where it runs | When you install it |
|---|---|---|
| Git and Git Bash | Windows | Week 1 |
| VS Code | Windows | Week 1 |
| uv and Python 3.12 | Windows | Week 1 |
| WSL 2 (a Linux system inside Windows) | Windows; Docker Desktop runs on it | Week 2 |
| Docker Desktop | Windows, with the WSL 2 engine | Week 2 |
| Node.js 24 and npm | Windows | Week 2 |
| The course kit | Windows, in your home folder: `~/fspy-v3-kit` | Week 2 |
| AWS CLI version 2 | Windows | Map weeks, when your task asks for it |

Run every course command in **Git Bash**, unless a step says PowerShell.

## Part 1, week 1: Git, VS Code, uv and Python

### Step 1: Git for Windows

You installed Git in week 1, from https://git-scm.com/downloads/win with the default options. Those options include Git Bash and Git Credential Manager (for signing in to GitHub).

Check it in Git Bash:

```bash
git --version
```

You see `git version 2.` and more numbers. Any version from 2.45 is fine.

### Step 2: VS Code and its Python extension

1. Install VS Code from https://code.visualstudio.com/download with the default options.
2. Open VS Code, select **Extensions** (Ctrl+Shift+X), search for **Python** and install the extension from Microsoft.

Check it in Git Bash: `code --version` prints a version number.

### Step 3: Make Git Bash the terminal in VS Code

1. In VS Code, press Ctrl+Shift+P and type `Terminal: Select Default Profile`.
2. Choose **Git Bash**.

This is the same as the setting `"terminal.integrated.defaultProfile.windows": "Git Bash"`.

Check it: open a new terminal with Ctrl+`. The prompt shows `MINGW64`, and `uname -s` prints a line that starts with `MINGW64`.

### Step 4: Line endings

Windows ends each line of a text file with two characters (CRLF), and Linux ends it with one (LF).
Linux containers need LF: a script saved with CRLF fails inside a container with errors such as `$'\r': command not found`.

1. In VS Code, open **Settings** (Ctrl+,) and search for `eol`.
2. Set **Files: Eol** to `\n`. This is the setting `"files.eol": "\n"`.

Check it: open a new file. The status bar at the bottom right shows `LF`, not `CRLF`.
Your course repository's `.gitattributes` file (week 2) keeps Git on LF as well.

### Step 5: uv and Python 3.12

uv installs Python and runs your programs. Run this in **PowerShell**:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Close every terminal and VS Code, then open Git Bash again and run:

```bash
uv --version
uv python install 3.12
```

Check it:

```bash
uv run --python 3.12 python --version
```

You see `Python 3.12.` and more numbers. uv's Python is the only Python you need. When a course command says `uv run`, uv starts this Python for you.

### Step 6: Python and UTF-8

In Git Bash, Python cannot print characters such as `₹` or `█` through a pipe or into a file, unless UTF-8 mode is on.
Turn it on once, in **PowerShell**:

```powershell
setx PYTHONUTF8 1
```

Then close and reopen VS Code and Git Bash.

Check it in Git Bash:

```bash
uv run python -c "print('₹1,250.50 █')" | cat
```

You see `₹1,250.50 █`. An error that names `charmap` means the setting is not on yet: reopen VS Code.

## Part 2, week 2: the course kit, WSL 2, Docker Desktop and Node.js

### Step 7: Clone the course kit

In Git Bash:

```bash
cd ~ && git clone https://github.com/Anaxionai/fspy-v3-kit.git
```

This makes the folder `~/fspy-v3-kit`, which is `C:\Users\<your name>\fspy-v3-kit`.
Keep it next to your course repository, never inside it. When a task says so, update it with `git pull` in that folder.

Check it: `ls ~/fspy-v3-kit` lists `README.md`, `VERSIONS.md`, `setup` and `data`.

### Step 8: WSL 2

WSL 2 runs a real Linux system inside Windows. Docker Desktop uses it to run containers.
Open **PowerShell as administrator** (right-click PowerShell and choose "Run as administrator") and run:

```powershell
wsl --install
```

Restart the laptop when it asks. Ubuntu then opens and asks for a user name and a password. Choose a short name, such as `asha`, and a password you will remember. The course does not need Ubuntu, so you can close it after this.

Check it in PowerShell:

```powershell
wsl --version
wsl -l -v
```

`wsl --version` shows `WSL version: 2.` and more numbers: it must be 2.1.5 or newer. If it is older, run `wsl --update`.
`wsl -l -v` lists Ubuntu with `VERSION 2`.

### Step 9: Limit WSL 2's memory

Docker Desktop runs inside WSL 2, so this limit keeps Docker and every container to 4 GB.
That leaves enough memory for Windows, VS Code and your browser on an 8 GB laptop.

In Git Bash, copy the kit's settings file to your Windows user folder:

```bash
cp ~/fspy-v3-kit/setup/wslconfig.example ~/.wslconfig
cat ~/.wslconfig
```

Then, in PowerShell, stop WSL so that it starts again with the limit:

```powershell
wsl --shutdown
```

Wait 8 seconds before you start Docker Desktop again. On a laptop with 16 GB of memory, change `memory=4GB` to `memory=8GB` in `~/.wslconfig`.
You check the limit in Step 10, once Docker Desktop runs.

### Step 10: Docker Desktop

Docker Desktop runs containers on Windows, using WSL 2.
**Licence:** Docker Desktop is free under the Personal plan for individual learning. It is also free for small businesses with fewer than 250 employees and less than $10 million in yearly revenue.

1. Download **Docker Desktop for Windows (x86_64)** from https://docs.docker.com/desktop/setup/install/windows-install/.
2. Run the installer. Keep **Use WSL 2 instead of Hyper-V** ticked, then finish. Restart the laptop if it asks.
3. Start **Docker Desktop** from the Start menu.
4. Accept the Docker Subscription Service Agreement. Signing in is optional: you may skip it.
5. Wait until the bottom left of the Docker Desktop window says **Engine running**.

Check it in Git Bash:

```bash
docker run hello-world
docker compose version
docker info | grep "Total Memory"
```

- `docker run hello-world` prints `Hello from Docker!` and a few lines that explain what happened.
- `docker compose version` prints `Docker Compose version` and a number.
- `Total Memory` is about `3.8GiB`: that is your 4 GB limit from Step 9. If it shows more, run `wsl --shutdown` in PowerShell, wait 8 seconds and start Docker Desktop again.

Docker Desktop must be running whenever you use Docker. Start it from the Start menu after you restart the laptop.

### Step 11: Git Bash and Docker: the path rule

Git Bash changes any word that looks like a Linux path, such as `/etc` or `/tmp/file.sql`, into a Windows path before Docker sees it.
So this command fails, because Docker receives `C:/Program Files/Git/etc`:

```bash
docker run --rm alpine ls /etc
```

When a `docker` command names a path inside a container, put `MSYS_NO_PATHCONV=1` in front of it. This works:

```bash
MSYS_NO_PATHCONV=1 docker run --rm alpine ls /etc
MSYS_NO_PATHCONV=1 docker run --rm -v "$PWD":/work alpine ls /work
```

- Put `MSYS_NO_PATHCONV=1` in front of one command at a time. Never set it for the whole terminal with `export`: then `uv run ~/file.py` and other commands break.
- With the prefix, give files on your laptop as relative paths, such as `data/stations.sql`, not `~/...`.
- You do not need it for paths inside quotes after `sh -c`, such as `docker exec web sh -c 'ls /tmp'`, or for paths inside a Compose file.
- Interactive commands such as `docker exec -it ...` work in VS Code's terminal. In the separate Git Bash window, put `winpty` in front if you see `the input device is not a TTY`.

### Step 12: Node.js 24 LTS

The course uses Node.js 24, a long-term support (LTS) version.

1. Open https://nodejs.org/en/download and choose **v24 (LTS)**, **Windows** and **x64**. Download the **Windows Installer (.msi)**.
2. Run it with the default options. Leave **Automatically install the necessary tools** unticked.
3. Close and reopen VS Code.

Do not use `winget install OpenJS.NodeJS.LTS`: it now installs version 26, not 24.

Check it in Git Bash:

```bash
node --version
npm --version
```

`node --version` prints `v24.` and more numbers. Version 24 or newer is fine. `npm --version` prints a version number.

### Step 13: AWS CLI version 2 (map weeks)

Install this when your map-week task asks for it. Choose one way:

- **The Windows installer** (needs an administrator account): download and run https://awscli.amazonaws.com/AWSCLIV2.msi with the default options.
- **Without administrator rights**: run this in PowerShell: `irm https://awscli.amazonaws.com/v2/install.ps1 | iex`

Then reopen Git Bash and check it:

```bash
aws --version
```

You see `aws-cli/2.` and more numbers. The course uses the AWS CLI only with fake keys, against the cloud lab's AWS emulator.

## Final check

Run these in Git Bash, in VS Code's terminal. Compare each line with the "You see" column.

| Command | You see |
|---|---|
| `git --version` | `git version 2.` and more |
| `uv run --python 3.12 python --version` | `Python 3.12.` and more |
| `node --version` | `v24.` or newer |
| `npm --version` | a version number |
| `docker run hello-world` | `Hello from Docker!` |
| `docker info \| grep "Total Memory"` | about `3.8GiB` (or about `7.7GiB` with `memory=8GB`) |
| `cat ~/.wslconfig` | `memory=4GB` and `swap=2GB` |
| `ls ~/fspy-v3-kit` | `README.md`, `VERSIONS.md` and the kit folders |

## Ubuntu (optional)

`wsl --install` also installed Ubuntu. The course does not need it, because every tool runs on Windows.
You may use it to practise Linux commands: type `wsl` in PowerShell to open it, and `exit` to leave.

## If something goes wrong

| What you see | What to do |
|---|---|
| `uv`, `node`, `npm` or `aws` is not recognised | The terminal was open before the install. Close every terminal and VS Code, then open them again. |
| `wsl --install` says that virtualisation is off | Turn on Intel VT-x or AMD SVM in the BIOS. Ask your mentor if you are unsure. |
| Docker Desktop says WSL needs an update | Run `wsl --update` in PowerShell, then start Docker Desktop again. |
| `error during connect` or `Is the docker daemon running?` | Start Docker Desktop and wait for **Engine running**. |
| An error shows a path such as `C:/Program Files/Git/...` | Add `MSYS_NO_PATHCONV=1` in front of the `docker` command (Step 11). |
| `the input device is not a TTY` | Run the command in VS Code's terminal, or put `winpty` in front of it. |
| `UnicodeEncodeError` and `charmap` | Do Step 6, then reopen VS Code. |
| `$'\r': command not found` or `bad interpreter` | The file has CRLF line endings. In VS Code, select `CRLF` in the status bar, choose `LF` and save. Then do Step 4. |
| `port is already allocated` for 5432 | Another PostgreSQL runs on your laptop. Stop it in Windows Services, or ask your mentor. |
| The laptop is slow while Docker runs | Check Step 9, and stop the cloud lab profiles you are not using. |

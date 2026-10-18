# Lesson 2: Command line and git

Goal: move around in a terminal, and use git to save, share, and submit your work.

## The command line

You type commands into a terminal. The ones you need:

| Command | Does |
|---|---|
| `pwd` | print the folder you are in |
| `ls` | list files (`dir` on Windows Command Prompt) |
| `cd folder` | move into a folder |
| `cd ..` | move up one folder |
| `mkdir name` | make a folder |
| `cat file` | print a file's contents (`type file` on Windows) |

On Windows, use Git Bash or WSL so these commands work as written.

Tips: press Tab to auto-complete file names, and press the up arrow to bring back the previous command.

## Virtual environments

A virtual environment is a private set of Python packages for one project, so projects do not break each other.

```bash
python -m venv .venv                 # create (once)
source .venv/bin/activate            # activate (every new terminal)
pip install -r requirements.txt      # install the project's packages
deactivate                           # leave it
```

When your prompt shows `(.venv)`, it is active. If you ever get `ModuleNotFoundError`, check that first.

## Why git

Git records snapshots of your project so you can go back, see what changed, and work with others without overwriting each other. GitHub hosts a shared copy.

## The everyday cycle

```bash
git clone <url>          # get a copy of a repo (once)
git status               # what has changed?
git add file.py          # stage a change
git commit -m "Add cadence function"    # save a snapshot with a message
git push                 # upload to GitHub
git pull                 # download others' changes
```

A good commit message says what changed, in a short sentence that starts with a verb.

Check `git status` often. It is always safe and tells you exactly where you are.

## Branches

A branch is a separate line of work. Never work directly on `main`.

```bash
git checkout -b submit/00_python_tooling/yourusername   # create and switch
# ...edit, add, commit...
git push -u origin submit/00_python_tooling/yourusername
```

Then open a **pull request** on GitHub: a request to merge your branch into `main`, where a teammate can review it. This is how you submit checkpoints (see the root `CONTRIBUTING.md`).

## Things you should not commit

- Large or generated files (the `.gitignore` already skips `*.csv` and `*.png`)
- Anything private: passwords, API keys, participant data
- Your `.venv` folder

If you did commit something you should not have, tell a team lead rather than trying to hide it, because removing it properly takes care.

## When things go wrong

- **"Your branch is behind"**: run `git pull`.
- **Merge conflict**: git marks the conflicting lines in the file with `<<<<<<<`, `=======`, `>>>>>>>`. Edit the file to keep what you want, delete the markers, then `git add` and `git commit`. Ask for help the first time.
- **Committed to the wrong branch**: do not panic, and do not delete things. Ask someone.

## Try it

1. Make a practice folder, run `git init` in it, and create a `notes.txt`.
2. Make three commits with different changes.
3. Run `git log --oneline` and read your history.

For a hands-on tutorial, work through [Learn Git Branching](https://learngitbranching.js.org/).

Next: [numpy and pandas](03_numpy_and_pandas.md)

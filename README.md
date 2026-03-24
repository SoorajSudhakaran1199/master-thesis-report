# Master Thesis – LaTeX Repository

This repository contains the LaTeX source files for the Master’s thesis.

## Daily workflow: how to save your work to GitHub

Follow these steps **every time you finish working** on the thesis.

### 1) Finish editing

* Edit `.tex`, `.bib`, and figure files (`.png`, `.jpg`).
* You may compile locally to view the PDF (the PDF stays local and is **not** committed).

### 2) Check what changed

```bash
git status
```

You should normally see only source files (`.tex`, `.bib`, images). If you see build files (`.pdf`, `.aux`, `.xdv`, `.synctex`), just ignore them.

### 3) Commit your changes

```bash
git add -A
git commit -m "Update chapter X"
```

Use clear messages, for example:

* `Update chapter 2 (State of the Art)`
* `Add functional requirements table`
* `Fix citations and formatting`

### 4) Push to GitHub (backup)

```bash
git push
```

That’s it — your work is now safely backed up on GitHub.

### Do NOT run in daily work

These are one-time or advanced commands and should not be used day-to-day:

```bash
git rm -r --cached .
git rebase
git pull --rebase
git push --force
```

### Optional end-of-day check

```bash
git log -1
git status
```

Make sure the working tree is clean before you stop working.

## Setting up this thesis on another laptop (new machine checklist)

Follow these steps **once**, before you start working on a second laptop (e.g. home PC, university PC).

### A) Before you switch laptops (on the current machine)

Do this to make sure everything is safely stored.

1. Check that nothing is uncommitted

```bash
git status
```

It should say: `working tree clean`.

2. Commit and push any remaining work

```bash
git add -A
git commit -m "Final sync before switching laptop"
git push
```

3. Verify the latest commit is on GitHub

```bash
git log -1
```

You should see your most recent commit message.

---

### B) On the new laptop (first-time setup)

1. Install required software

* **Git**
* **TeX distribution** (TeX Live recommended)
* **VS Code** (recommended editor)
* VS Code extensions:

  * *LaTeX Workshop*
  * *GitLens* (optional)

2. Configure Git identity (once)

```bash
git config --global user.name "Your Name"
git config --global user.email "your@email.com"
```

3. Clone the repository

```bash
git clone https://github.com/SoorajSudhakaran1199/master-thesis-report.git
cd master-thesis-report
```

4. Open the project

```bash
code .
```

5. Test compilation

* Build using VS Code **LaTeX Workshop** or

```bash
xelatex main
biber main
xelatex main
```

Confirm that `main.pdf` is generated locally.

---

### C) Normal work on the new laptop

From now on, use the **same daily workflow**:

```bash
git status
git add -A
git commit -m "Updated chapter "
git push
```

---

### Important notes

* Do **not** copy the project using USB drives or cloud sync folders.
* GitHub is the **single source of truth**.
* PDFs and LaTeX build files are generated locally and are **not** synced.
* Always `git pull` before starting work if you used another laptop last time.

```bash
git pull
```
xelatex main.tex
biber main
xelatex main.tex
xelatex main.tex

######

When adding a NEW reference

Ctrl + Alt + B

(or use latexmk (xelatex + biber))

latexmk -pdfxe main.tex

again ctrl+ s 
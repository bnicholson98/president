# Git Setup in VS Code

This guide will walk you through setting up this repository with Git in Visual Studio Code.

## Prerequisites

- Visual Studio Code installed
- Git installed on your system
- GitHub/GitLab/Bitbucket account (if you want to push to a remote repository)

## Step-by-Step Setup

### 1. Install Git (if not already installed)

**Windows:**
- Download from https://git-scm.com/download/win
- Run installer with default settings

**MacOS:**
```bash
brew install git
```
Or use Xcode command line tools:
```bash
xcode-select --install
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install git
```

### 2. Configure Git (First Time Only)

Open terminal in VS Code (Terminal → New Terminal) and run:

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### 3. Initialize Local Git Repository

In VS Code:

**Option A: Using the Terminal**

1. Open the integrated terminal (`` Ctrl+` `` or Terminal → New Terminal)
2. Navigate to your project folder:
   ```bash
   cd path/to/president
   ```
3. Initialize Git:
   ```bash
   git init
   ```

**Option B: Using VS Code UI**

1. Open the project folder (File → Open Folder)
2. Click the Source Control icon in the left sidebar (or press `Ctrl+Shift+G`)
3. Click "Initialize Repository" button

### 4. Create .gitignore File

Create a `.gitignore` file in your project root with the following content:

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
env/
ENV/
.venv

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Testing
.pytest_cache/
.coverage
htmlcov/
.tox/

# OS
.DS_Store
Thumbs.db
```

**To create .gitignore in VS Code:**
1. Click "New File" icon in Explorer
2. Name it `.gitignore`
3. Paste the content above
4. Save (Ctrl+S)

### 5. Make Your First Commit

**Option A: Using the Terminal**

```bash
# Add all files to staging
git add .

# Create your first commit
git commit -m "Initial commit: Add README and Implementation Guide"
```

**Option B: Using VS Code UI**

1. Open Source Control panel (Ctrl+Shift+G)
2. You'll see all changed files listed
3. Hover over "Changes" and click the "+" icon to stage all files
   - Or click "+" next to individual files to stage them
4. Enter a commit message in the text box at the top (e.g., "Initial commit: Add README and Implementation Guide")
5. Click the checkmark icon above the message box (or press Ctrl+Enter)

### 6. Create Remote Repository (Optional)

If you want to push to GitHub/GitLab/Bitbucket:

**For GitHub:**

1. Go to https://github.com
2. Click "+" in top right → "New repository"
3. Name it "president" (or your preferred name)
4. Don't initialize with README (you already have one)
5. Click "Create repository"
6. Copy the repository URL (e.g., `https://github.com/yourusername/president.git`)

**For GitLab:**
1. Go to https://gitlab.com
2. Click "New project" → "Create blank project"
3. Name it and create

**For Bitbucket:**
1. Go to https://bitbucket.org
2. Click "Create" → "Repository"
3. Name it and create

### 7. Connect Local Repository to Remote

In VS Code terminal:

```bash
# Add remote repository
git remote add origin https://github.com/yourusername/president.git

# Verify remote was added
git remote -v

# Push your code (first time)
git push -u origin main
```

**Note:** If your default branch is named "master" instead of "main", use:
```bash
git branch -M main  # Rename to main
git push -u origin main
```

### 8. Working with Git in VS Code

#### Daily Workflow:

**Making Changes:**
1. Edit your files
2. Modified files appear in Source Control panel with an "M" marker
3. New files appear with a "U" (untracked) marker

**Committing Changes:**
1. Open Source Control (Ctrl+Shift+G)
2. Stage files (click "+" icon)
3. Enter commit message
4. Click checkmark to commit

**Pushing to Remote:**
1. Click "..." menu in Source Control panel
2. Select "Push"
   - Or use terminal: `git push`

**Pulling from Remote:**
1. Click "..." menu in Source Control panel
2. Select "Pull"
   - Or use terminal: `git pull`

#### Useful VS Code Git Features:

**View File Changes:**
- Click on a file in Source Control panel to see diff

**View Git History:**
- Install "Git Graph" or "GitLens" extension for better visualization
- Extensions → Search "GitLens" → Install

**Create Branches:**
1. Click branch name in bottom-left status bar
2. Select "Create new branch"
3. Enter branch name

**Switch Branches:**
1. Click branch name in bottom-left status bar
2. Select branch to switch to

### 9. Recommended VS Code Extensions

Install these for better Git experience:

1. **GitLens** - Supercharge Git in VS Code
   - View commit history, file history, line blame, and more
   
2. **Git Graph** - View a Git graph of your repository
   
3. **Git History** - View git log, file history, compare branches

**To Install:**
1. Click Extensions icon in left sidebar (or Ctrl+Shift+X)
2. Search for extension name
3. Click Install

### 10. Common Git Commands (Terminal Reference)

```bash
# Check status
git status

# View changes
git diff

# Stage specific file
git add filename.py

# Stage all files
git add .

# Commit with message
git commit -m "Your message"

# Push to remote
git push

# Pull from remote
git pull

# View commit history
git log

# View branches
git branch

# Create and switch to new branch
git checkout -b feature-name

# Switch to existing branch
git checkout branch-name

# Merge branch into current branch
git merge branch-name

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Discard all local changes
git reset --hard HEAD
```

### 11. Best Practices

1. **Commit often** - Make small, logical commits
2. **Write clear commit messages** - Describe what and why
3. **Pull before push** - Always pull latest changes before pushing
4. **Use branches** - Create feature branches for new development
5. **Review before commit** - Check what you're committing in the diff view
6. **Don't commit sensitive data** - Use .gitignore properly

### 12. Commit Message Conventions

Use clear, descriptive commit messages:

```
Good examples:
- "Add Card class with rank and suit attributes"
- "Implement deck shuffling and dealing logic"
- "Fix bug in trick winner determination"
- "Update README with installation instructions"

Bad examples:
- "fixed stuff"
- "wip"
- "Update"
```

### 13. Troubleshooting

**Problem: "permission denied" when pushing**
- Solution: Check your GitHub credentials or use SSH keys

**Problem: Merge conflicts**
- Solution: VS Code highlights conflicts in files
  - Choose "Accept Current Change", "Accept Incoming Change", or edit manually
  - Stage the resolved files and commit

**Problem: Want to undo a commit**
```bash
# Undo last commit but keep changes
git reset --soft HEAD~1

# Undo last commit and discard changes
git reset --hard HEAD~1
```

**Problem: Accidentally committed to wrong branch**
```bash
# On wrong branch
git reset --soft HEAD~1  # Undo commit, keep changes
git stash                # Save changes temporarily

# Switch to correct branch
git checkout correct-branch
git stash pop           # Apply saved changes
git add .
git commit -m "Your message"
```

### 14. Next Steps

1. ✅ Initialize repository
2. ✅ Make first commit
3. ✅ Set up remote (optional)
4. ✅ Install helpful extensions
5. 🎯 Start implementing the game (see IMPLEMENTATION_GUIDE.md)

---

## Quick Reference Card

| Action | VS Code UI | Terminal Command |
|--------|-----------|------------------|
| Initialize repo | Source Control → Initialize | `git init` |
| Stage all files | Click + on "Changes" | `git add .` |
| Commit | Type message + checkmark | `git commit -m "message"` |
| Push | ... menu → Push | `git push` |
| Pull | ... menu → Pull | `git pull` |
| View history | Timeline view or GitLens | `git log` |
| Create branch | Click branch name → Create | `git checkout -b name` |
| Switch branch | Click branch name → Select | `git checkout name` |

---

Happy coding! 🚀

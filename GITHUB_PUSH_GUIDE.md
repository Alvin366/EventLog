# GitHub Push Guide - EventLog to Main

Complete step-by-step commands to push EventLog to GitHub main branch.

**Status**: Fresh repository (no commits yet)
**Target**: https://github.com/Alvin366/EventLog
**Branch**: main

---

## Prerequisites Check

Before you start, verify:

```bash
# Check git is installed
git --version
# Should show: git version 2.x.x or higher

# Check you're in EventLog directory
pwd
# Should end with: /config/ClaudeProjects/EventLog

# Check directory has files
ls -la
# Should show: all EventLog files and directories
```

---

## Step 1: Initialize Git Repository Locally

```bash
# Navigate to EventLog directory
cd /config/ClaudeProjects/EventLog

# Initialize git repository
git init

# Verify .git directory created
ls -la | grep .git
```

**Expected output**:
```
drwxr-xr-x  ... .git
```

---

## Step 2: Configure Git (First Time Only)

```bash
# Set your Git username globally (one time)
git config --global user.name "Alvin366"

# Set your Git email globally (one time)
git config --global user.email "your-email@example.com"

# Verify configuration
git config --global user.name
git config --global user.email
```

**Replace with**:
- `Alvin366` - Your GitHub username
- `your-email@example.com` - Your GitHub email

---

## Step 3: Add All Files to Staging Area

```bash
# Add all files to git
git add .

# Verify files are staged
git status
```

**Expected output**:
```
On branch master

No commits yet

Changes to be committed:
  (use "rm --cached <file>..." to unstage)
    new file:   00_START_HERE.md
    new file:   CHANGELOG.md
    new file:   DEPLOYMENT_CHECKLIST.md
    ... (all your files)
```

---

## Step 4: Create Initial Commit

```bash
# Create initial commit with descriptive message
git commit -m "feat: Initial EventLog MVP commit

- EventLogCollector custom component for HA Core log monitoring
- Event logger blueprint for processing and deduplication
- Event management scripts (log, acknowledge, close)
- Helper configurations (input_text, input_select, input_boolean, input_number)
- Valiug dashboard card integration
- Complete documentation and deployment guides
- Version 0.1.0-MVP ready for testing

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>"

# Verify commit was created
git log --oneline
```

**Expected output**:
```
abc1234 feat: Initial EventLog MVP commit
```

---

## Step 5: Rename Branch to Main (If Needed)

```bash
# Check current branch name
git branch
# Shows: * master (or main)

# If it shows "master", rename to "main"
git branch -M main

# Verify new name
git branch
# Shows: * main
```

---

## Step 6: Add Remote Repository

```bash
# Add GitHub as remote origin
git remote add origin https://github.com/Alvin366/EventLog.git

# Verify remote is added
git remote -v
```

**Expected output**:
```
origin  https://github.com/Alvin366/EventLog.git (fetch)
origin  https://github.com/Alvin366/EventLog.git (push)
```

---

## Step 7: Push to GitHub Main Branch

### Option A: HTTPS (Recommended for first time)

```bash
# Push to main branch
git push -u origin main

# When prompted for password/token, enter your GitHub token
# (Create token at: https://github.com/settings/tokens)
```

**If you see**:
```
Username for 'https://github.com': Alvin366
Password for 'https://Alvin366@github.com': (paste your token here)
```

Then you're being authenticated correctly!

### Option B: SSH (If you have SSH key set up)

```bash
# First, check if you have SSH key
cat ~/.ssh/id_rsa.pub

# If key exists, use SSH URL instead
git remote remove origin
git remote add origin git@github.com:Alvin366/EventLog.git

# Push to main
git push -u origin main
```

---

## Step 8: Verify Push Succeeded

### Via Command Line

```bash
# Check push status
git log -1 --oneline
# Should show your commit

# Check remote branch
git branch -r
# Should show: origin/main

# Check status
git status
# Should show: "On branch main, Your branch is up to date with 'origin/main'."
```

### Via GitHub Website

1. Open: https://github.com/Alvin366/EventLog
2. You should see:
   - ✅ All files uploaded
   - ✅ Initial commit listed
   - ✅ Branch shows "main"
   - ✅ Code visible in repo

---

## Complete Command Sequence (Copy & Paste)

```bash
# Step 1-2: Setup
cd /config/ClaudeProjects/EventLog
git init
git config --global user.name "Alvin366"
git config --global user.email "your-email@example.com"

# Step 3: Stage files
git add .

# Step 4: Commit
git commit -m "feat: Initial EventLog MVP commit

- EventLogCollector custom component for HA Core log monitoring
- Event logger blueprint for processing and deduplication
- Event management scripts (log, acknowledge, close)
- Helper configurations (input_text, input_select, input_boolean, input_number)
- Valiug dashboard card integration
- Complete documentation and deployment guides
- Version 0.1.0-MVP ready for testing

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>"

# Step 5: Rename branch
git branch -M main

# Step 6: Add remote
git remote add origin https://github.com/Alvin366/EventLog.git

# Step 7: Push to main
git push -u origin main

# Step 8: Verify
git log -1 --oneline
git status
```

---

## Troubleshooting

### "error: repository not empty"
```bash
# If .git already exists, remove it
rm -rf .git

# Start from Step 1 again
git init
```

### "fatal: could not read Username"
You need GitHub authentication:
1. Go to: https://github.com/settings/tokens
2. Create new token (Classic)
3. Give it "repo" permissions
4. Copy the token
5. When prompted for password, paste the token

### "remote origin already exists"
```bash
# Remove old remote
git remote remove origin

# Add correct remote
git remote add origin https://github.com/Alvin366/EventLog.git
```

### "Permission denied (publickey)"
You're using SSH without key set up:
```bash
# Switch to HTTPS
git remote remove origin
git remote add origin https://github.com/Alvin366/EventLog.git
git push -u origin main
```

### "fatal: no changes added to commit"
Make sure files are staged:
```bash
git add .
git status  # Verify files show under "Changes to be committed"
```

### "error: src refspec main does not match any"
Your branch isn't named "main":
```bash
# Check current branch
git branch

# Rename if needed
git branch -M main

# Try push again
git push -u origin main
```

### "Everything up-to-date"
Means your commits already pushed. To verify:
```bash
git log -1
git remote -v
```

---

## After Push Successful

### Verify on GitHub

```bash
# Check repository on GitHub
open https://github.com/Alvin366/EventLog
# Or use browser and navigate to the URL
```

Should show:
- ✅ All files present
- ✅ Directory structure intact
- ✅ README.md displayed
- ✅ Initial commit in history
- ✅ Branch set to "main"

### Set Up Repository (Optional but Recommended)

Once pushed, you can:

1. **Create branch protection** (GitHub settings):
   - Settings → Branches → Require status checks

2. **Add GitHub Actions** (CI/CD):
   - Create `.github/workflows/test.yml`
   - Create `.github/workflows/lint.yml`

3. **Add collaborators**:
   - Settings → Collaborators
   - Add team members or agents

4. **Create project board**:
   - Projects → New project
   - Add Phase 2 tasks

---

## Useful Git Commands After Push

```bash
# See commit history
git log --oneline -10

# See what's different from main
git diff main

# Create a new branch for development
git checkout -b feature/add-plant-monitor

# Push new branch
git push -u origin feature/add-plant-monitor

# Switch back to main
git checkout main

# Update main from remote
git pull origin main

# See all branches
git branch -a

# Delete local branch (after merged)
git branch -d feature/add-plant-monitor

# Delete remote branch
git push origin --delete feature/add-plant-monitor
```

---

## CI/CD Setup (Optional)

Create `.github/workflows/lint.yml`:

```yaml
name: Lint YAML Files

on: [push, pull_request]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Lint YAML
        run: |
          find . -name "*.yaml" -type f | xargs yamllint -d relaxed
```

Create `.github/workflows/docs.yml`:

```yaml
name: Verify Documentation

on: [push, pull_request]

jobs:
  docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Check documentation exists
        run: |
          test -f README.md
          test -f docs/ARCHITECTURE.md
          test -f docs/CONFIGURATION_GUIDE.md
```

Then push these files:
```bash
git add .github/workflows/
git commit -m "ci: Add GitHub Actions workflows"
git push origin main
```

---

## Summary Checklist

- [ ] Git installed (`git --version`)
- [ ] In EventLog directory (`pwd` ends with EventLog)
- [ ] Files present (`ls -la` shows files)
- [ ] Repository initialized (`git init`)
- [ ] Git configured (`git config --global user.name`)
- [ ] Files staged (`git add .`)
- [ ] Committed (`git commit`)
- [ ] Branch renamed to main (`git branch -M main`)
- [ ] Remote added (`git remote add origin`)
- [ ] Pushed to GitHub (`git push -u origin main`)
- [ ] Verified on GitHub website
- [ ] Repository shows all files and history

---

## Need Help?

### Check Git status anytime:
```bash
git status
```

### See what will be pushed:
```bash
git log -1 --stat
```

### See all commits:
```bash
git log --oneline
```

### Undo last commit (before push):
```bash
git reset --soft HEAD~1
# Files go back to staged area
```

### Undo last commit (after push):
```bash
# You'll need to force push (be careful!)
git reset --hard HEAD~1
git push --force origin main
```

---

## Success Criteria

✅ EventLog repository appears on GitHub.com
✅ All 26 files visible in repository
✅ Directory structure intact (blueprints/, scripts/, config/, etc.)
✅ README.md displays on main page
✅ Commit history shows initial commit
✅ Branch shows as "main"
✅ Can clone locally: `git clone https://github.com/Alvin366/EventLog.git`

---

## Your Next Step

Run the "Complete Command Sequence" section above (copy and paste all commands together), or run them one section at a time.

**Then verify**: Open https://github.com/Alvin366/EventLog in browser. You should see all your EventLog files! 🎉

---

**Guide Version**: 1.0
**Date Created**: 2024-10-30
**Status**: Ready to execute

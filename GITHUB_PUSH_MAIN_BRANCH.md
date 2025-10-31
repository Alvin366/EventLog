# EventLog v2 - Push to GitHub Main Branch

**Purpose**: Push v2 code to GitHub main branch (replacing v1)
**Time Required**: 10-15 minutes
**Status**: Step-by-step procedure

---

## Prerequisites

✅ Git installed on system
✅ GitHub repository created: https://github.com/Alvin366/EventLog
✅ Local repository at: `/config/ClaudeProjects/EventLog`
✅ All v1 files removed from project
✅ v2 component files ready in `/config/custom_components/eventlog/`

---

## Step 1: Check Repository Status

Open terminal/SSH and navigate to the project:

```bash
cd /config/ClaudeProjects/EventLog
```

Check current git status:

```bash
git status
```

**Expected output** (shows untracked/modified files):
```
On branch main (or develop)
...
Untracked files:
  custom_components/eventlog/
  INSTALL_NOW.md
  START_HERE.md
  etc.
```

Check current branches:

```bash
git branch -a
```

**Expected output**:
```
* main          (or your current branch)
  origin/main
```

---

## Step 2: Create New Branch for v2

Create a new branch called `v2-main`:

```bash
git checkout -b v2-main
```

Verify you're on the new branch:

```bash
git branch
```

**Expected output**:
```
  main
* v2-main
```

---

## Step 3: Add All v2 Files to Staging

Stage all the new v2 files:

```bash
git add -A
```

Verify files are staged:

```bash
git status
```

**Expected output** (shows files ready to commit):
```
On branch v2-main
Changes to be committed:
  new file: custom_components/eventlog/__init__.py
  new file: custom_components/eventlog/manifest.json
  new file: custom_components/eventlog/services.yaml
  new file: START_HERE.md
  new file: INSTALL_NOW.md
  ... (other new v2 files)

Deleted:
  deleted: blueprints/event_logger.yaml
  deleted: blueprints/eventlog_event_source.yaml
  ... (v1 files removed)
```

---

## Step 4: Commit Changes

Create a comprehensive commit message:

```bash
git commit -m "feat: Redesign EventLog v2 - Custom Component with InfluxDB

- Replace blueprint approach with custom component
- Implement automatic log file monitoring
- Add InfluxDB time-series storage backend
- Create 4-service API (log_event, query_events, acknowledge, close)
- Add complete installation and testing documentation
- Remove v1 blueprint files and obsolete documentation
- Supports unlimited event scalability

BREAKING CHANGE: v1 blueprint approach no longer used.
New installation from GitHub custom_components/eventlog/"
```

Or use simpler version:

```bash
git commit -m "refactor: Redesign EventLog as custom component with InfluxDB storage"
```

Verify commit was created:

```bash
git log --oneline -5
```

**Expected output** (shows your new commit):
```
abc1234 refactor: Redesign EventLog as custom component with InfluxDB storage
def5678 previous commit...
```

---

## Step 5: Push to GitHub (New Branch First - SAFE)

Push the new branch to GitHub first (safe way to verify):

```bash
git push -u origin v2-main
```

**Expected output**:
```
Enumerating objects...
Counting objects...
...
To https://github.com/Alvin366/EventLog.git
 * [new branch]      v2-main -> v2-main
Branch 'v2-main' set up to track remote branch 'v2-main' from 'origin'.
```

---

## Step 6: Verify on GitHub

1. Open: https://github.com/Alvin366/EventLog
2. Check **Branches** dropdown
3. You should see: `v2-main` branch
4. Click `v2-main` branch to view files
5. Verify:
   - ✅ `custom_components/eventlog/` exists with 4 files
   - ✅ New v2 documentation files present
   - ✅ Old v1 blueprint files removed
   - ✅ Commit message shows in history

---

## Step 7: Create Pull Request (Optional but Recommended)

On GitHub:

1. Go to **Pull Requests** tab
2. Click **New Pull Request**
3. Base branch: `main`
4. Compare branch: `v2-main`
5. Title: `Redesign: EventLog v2 Custom Component + InfluxDB`
6. Description:
   ```
   ## Summary
   Complete redesign from v1 blueprint approach to v2 custom component.

   ### Changes
   - Custom component with automatic log monitoring
   - InfluxDB storage backend
   - 4-service API for event management
   - Complete documentation suite
   - All v1 blueprint files removed

   ### Migration
   - Users must uninstall v1 (blueprints/helpers/automations)
   - Install v2 custom component from GitHub
   - See INSTALL_NOW.md for instructions

   ### Breaking Changes
   - v1 blueprint approach no longer used
   - Installation method completely changed
   ```
7. Click **Create Pull Request**
8. Review the changes
9. Click **Merge Pull Request** to merge into main

---

## Step 8: Merge v2-main into main

### Option A: Via GitHub Web UI (Recommended for Visibility)

1. Go to your Pull Request (from Step 7)
2. Click green **Merge Pull Request** button
3. Choose merge strategy (default is fine)
4. Confirm merge
5. Delete branch `v2-main` after merge

### Option B: Via Command Line

If you prefer command line:

```bash
# Switch to main branch
git checkout main

# Pull latest from remote
git pull origin main

# Merge v2-main into main
git merge v2-main

# Push merged main to GitHub
git push origin main

# Delete local v2-main branch
git branch -d v2-main

# Delete remote v2-main branch
git push origin --delete v2-main
```

---

## Step 9: Verify Main Branch Updated

On GitHub:

1. Go to repository main page
2. Click **Code** tab
3. Verify you're on `main` branch (dropdown at top)
4. Verify files show v2:
   - ✅ `custom_components/eventlog/` with 4 files
   - ✅ New documentation files
   - ✅ Old v1 files removed
5. Check commit history shows your v2 commit

---

## Step 10: Tag Release (Optional but Recommended)

Create a release tag:

```bash
git tag -a v2.0.0-alpha -m "EventLog v2.0.0-alpha - Custom Component Release"
```

Push tag to GitHub:

```bash
git push origin v2.0.0-alpha
```

On GitHub:

1. Go to **Releases** tab
2. You should see `v2.0.0-alpha`
3. Click to view release details

---

## Summary of Changes

After completing all steps:

✅ **GitHub main branch** contains v2 code
✅ **v2 installation** available via: `git clone https://github.com/Alvin366/EventLog.git`
✅ **v1 files** completely removed from repository
✅ **Documentation** up-to-date for v2
✅ **Release tag** created for v2.0.0-alpha
✅ **Pull request** documents the redesign

---

## Rollback (If Needed)

If something goes wrong before pushing to main:

```bash
# Go back to previous state
git checkout main
git reset --hard origin/main

# Delete v2-main branch
git branch -D v2-main
git push origin --delete v2-main
```

---

## Commit Message Best Practices

Your commit message should explain:

- **What changed**: `Redesign EventLog from blueprint to custom component`
- **Why it changed**: `Blueprints couldn't store events reliably`
- **Breaking changes**: `v1 blueprint approach no longer supported`
- **How to upgrade**: `See INSTALL_NOW.md`

---

## Verification Checklist

- [ ] Created `v2-main` branch
- [ ] Staged all v2 files with `git add -A`
- [ ] Created meaningful commit message
- [ ] Pushed `v2-main` to GitHub
- [ ] Verified files on GitHub
- [ ] Created Pull Request (optional)
- [ ] Merged into `main` branch
- [ ] Verified `main` branch on GitHub has v2 files
- [ ] Created release tag (optional)
- [ ] Updated GitHub release notes

---

## Quick Command Summary

```bash
# Navigate to project
cd /config/ClaudeProjects/EventLog

# Check status
git status

# Create v2 branch
git checkout -b v2-main

# Stage all changes
git add -A

# Commit with message
git commit -m "refactor: Redesign EventLog as custom component with InfluxDB"

# Push new branch
git push -u origin v2-main

# Switch to main
git checkout main

# Merge v2-main into main
git merge v2-main

# Push updated main
git push origin main

# Delete v2-main
git branch -d v2-main
git push origin --delete v2-main

# Create release tag
git tag -a v2.0.0-alpha -m "EventLog v2.0.0-alpha Release"
git push origin v2.0.0-alpha
```

---

## Troubleshooting

### "fatal: Not a git repository"
```bash
# You're not in the right directory
cd /config/ClaudeProjects/EventLog
git status
```

### "Branch already exists"
```bash
# Delete the existing branch
git branch -D v2-main
# Then create new one
git checkout -b v2-main
```

### "Permission denied when pushing"
- Verify GitHub credentials
- Check SSH key is configured
- May need to use HTTPS instead of SSH

### "Merge conflicts"
```bash
# View conflicts
git status

# Edit conflicting files to resolve
# Then continue merge
git add .
git commit -m "Resolve merge conflicts"
```

---

## After Push Verification

1. **Test Installation**
   ```bash
   cd /tmp
   git clone https://github.com/Alvin366/EventLog.git test-install
   cd test-install
   ls custom_components/eventlog/
   # Should show: __init__.py, manifest.json, services.yaml, README.md
   ```

2. **Verify Documentation**
   - Check START_HERE.md exists
   - Check INSTALL_NOW.md exists
   - Check README.md is updated for v2

3. **Clean Up Test**
   ```bash
   rm -rf /tmp/test-install
   ```

---

**Version**: 2.0.0-alpha
**Status**: Ready to Push
**Date**: 2024-10-31

# EventLog v1 Cleanup - Remove Old Files

**Purpose**: Remove all v1 blueprint/automation/helper files
**Status**: Ready to remove
**Date**: 2024-10-31

---

## Files to Remove (v1 - Blueprint Approach)

### Blueprint Files
```
/config/ClaudeProjects/EventLog/blueprints/
├── event_logger.yaml           ← OLD (v1)
├── eventlog_event_source.yaml  ← OLD (v1)
├── eventlog_master.yaml        ← OLD (v1)
└── README.md                   ← OLD (v1)
```

### Example Files
```
/config/ClaudeProjects/EventLog/examples/
└── sample_events.yaml          ← OLD (v1)
```

### Total Files to Remove

- `blueprints/event_logger.yaml`
- `blueprints/eventlog_event_source.yaml`
- `blueprints/eventlog_master.yaml`
- `blueprints/README.md`
- `examples/sample_events.yaml`

### Optional Old Documentation to Remove

These are older guides that are no longer relevant:

- `00_START_HERE.md` - MVP overview (can keep for history)
- `PROJECT_SUMMARY.md` - MVP summary (can keep for history)
- `QUICK_START.md` - MVP quick start (can keep for history)
- `DEPLOYMENT_CHECKLIST.md` - MVP deployment (can remove)
- `INSTALL_AND_TEST.md` - MVP testing (can remove)
- `GITHUB_PUSH_GUIDE.md` - Old GitHub guide (can remove)
- `INDEX.md` - Old file index (can remove)
- `README_DEVELOPERS.md` - Old dev guide (can remove)
- `CHANGELOG.md` - Old changelog (can remove)
- `PUSH_COMPLETE.md` - Old push notes (can remove)
- `PUSH_TO_GITHUB_NOW.txt` - Old push notes (can remove)
- `GITHUB_PUSH_GUIDE.md` - Old push guide (can remove)

---

## Why Remove These?

✅ **v1 is obsolete** - Completely redesigned to v2
✅ **Confusing** - Old guides may mislead users
✅ **No longer used** - Blueprints don't work with v2
✅ **Cleaner** - Simplifies documentation
✅ **Professional** - Shows clear migration path

---

## What Stays (v2 - Custom Component Approach)

```
/config/ClaudeProjects/EventLog/
├── INSTALL_NOW.md                      ← NEW (v2)
├── GITHUB_INSTALLATION_QUICK.md         ← NEW (v2)
├── INSTALLATION_FROM_GITHUB.md          ← NEW (v2)
├── HOW_CUSTOM_COMPONENTS_WORK.md        ← NEW (v2)
├── GITHUB_SETUP_COMPLETE.md             ← NEW (v2)
├── V2_READY_FOR_TESTING.md              ← Keep
├── IMPLEMENTATION_V2.md                 ← Keep
├── REDESIGN_COMPLETE.md                 ← Keep
├── README.md                            ← Updated for v2
├── FILES_CREATED.md                     ← Keep
├── docs/
│   └── INFLUXDB_SCHEMA.md              ← Keep
└── custom_components/eventlog/          ← NEW v2 Component
    ├── __init__.py
    ├── manifest.json
    ├── services.yaml
    └── README.md
```

---

## Cleanup Command

### Option A: Remove Only v1 Blueprint/Example Files

```bash
# Safe removal - only removes v1 specific files
rm -f /config/ClaudeProjects/EventLog/blueprints/event_logger.yaml
rm -f /config/ClaudeProjects/EventLog/blueprints/eventlog_event_source.yaml
rm -f /config/ClaudeProjects/EventLog/blueprints/eventlog_master.yaml
rm -f /config/ClaudeProjects/EventLog/blueprints/README.md
rm -f /config/ClaudeProjects/EventLog/examples/sample_events.yaml

# Remove empty directories
rmdir /config/ClaudeProjects/EventLog/blueprints 2>/dev/null
rmdir /config/ClaudeProjects/EventLog/examples 2>/dev/null

echo "✅ v1 blueprint files removed"
```

### Option B: Remove v1 Blueprints + Old Documentation

```bash
# Remove v1 specific files
rm -f /config/ClaudeProjects/EventLog/blueprints/event_logger.yaml
rm -f /config/ClaudeProjects/EventLog/blueprints/eventlog_event_source.yaml
rm -f /config/ClaudeProjects/EventLog/blueprints/eventlog_master.yaml
rm -f /config/ClaudeProjects/EventLog/blueprints/README.md
rm -f /config/ClaudeProjects/EventLog/examples/sample_events.yaml

# Remove old MVP documentation
rm -f /config/ClaudeProjects/EventLog/DEPLOYMENT_CHECKLIST.md
rm -f /config/ClaudeProjects/EventLog/INSTALL_AND_TEST.md
rm -f /config/ClaudeProjects/EventLog/GITHUB_PUSH_GUIDE.md
rm -f /config/ClaudeProjects/EventLog/INDEX.md
rm -f /config/ClaudeProjects/EventLog/README_DEVELOPERS.md
rm -f /config/ClaudeProjects/EventLog/CHANGELOG.md
rm -f /config/ClaudeProjects/EventLog/PUSH_COMPLETE.md
rm -f /config/ClaudeProjects/EventLog/PUSH_TO_GITHUB_NOW.txt

# Remove empty directories
rmdir /config/ClaudeProjects/EventLog/blueprints 2>/dev/null
rmdir /config/ClaudeProjects/EventLog/examples 2>/dev/null

echo "✅ v1 files and old documentation removed"
```

---

## Before & After

### Before (With v1)
```
EventLog/
├── blueprints/           ← v1 (remove)
│   ├── event_logger.yaml
│   ├── eventlog_event_source.yaml
│   ├── eventlog_master.yaml
│   └── README.md
├── examples/             ← v1 (remove)
│   └── sample_events.yaml
├── old docs...           ← v1 (remove)
└── v2 docs...           ← keep
```

### After (Clean v2)
```
EventLog/
├── docs/
│   └── INFLUXDB_SCHEMA.md
├── custom_components/eventlog/
│   ├── __init__.py
│   ├── manifest.json
│   ├── services.yaml
│   └── README.md
├── INSTALL_NOW.md
├── GITHUB_INSTALLATION_QUICK.md
├── INSTALLATION_FROM_GITHUB.md
├── HOW_CUSTOM_COMPONENTS_WORK.md
├── V2_READY_FOR_TESTING.md
├── IMPLEMENTATION_V2.md
├── REDESIGN_COMPLETE.md
├── README.md
└── FILES_CREATED.md
```

---

## What About Home Assistant Config?

You may also have removed any v1 automations/helpers if you created them.

**Nothing to clean up in Home Assistant**:
- You never installed the v1 blueprint
- No automations were created
- No helpers were created

So no HA cleanup needed!

---

## Backup First?

Optional: Archive old files before deleting

```bash
# Create backup
mkdir -p /config/backups/EventLog-v1-backup
cp -r /config/ClaudeProjects/EventLog/blueprints /config/backups/EventLog-v1-backup/
cp -r /config/ClaudeProjects/EventLog/examples /config/backups/EventLog-v1-backup/
cp /config/ClaudeProjects/EventLog/DEPLOYMENT_CHECKLIST.md /config/backups/EventLog-v1-backup/
# ... etc for other old docs

echo "✅ Backup created at /config/backups/EventLog-v1-backup/"
```

---

## Verification

After cleanup, verify remaining files:

```bash
ls -la /config/ClaudeProjects/EventLog/

# Should show:
# - docs/ (with INFLUXDB_SCHEMA.md)
# - custom_components/eventlog/ (with 4 files)
# - INSTALL_NOW.md
# - GITHUB_INSTALLATION_QUICK.md
# - INSTALLATION_FROM_GITHUB.md
# - HOW_CUSTOM_COMPONENTS_WORK.md
# - GITHUB_SETUP_COMPLETE.md
# - V2_READY_FOR_TESTING.md
# - IMPLEMENTATION_V2.md
# - REDESIGN_COMPLETE.md
# - README.md
# - FILES_CREATED.md

# Should NOT show:
# - blueprints/ directory
# - examples/ directory
# - DEPLOYMENT_CHECKLIST.md
# - INSTALL_AND_TEST.md
# - etc.
```

---

## Summary

**Files to Remove** (5 files):
- blueprints/event_logger.yaml
- blueprints/eventlog_event_source.yaml
- blueprints/eventlog_master.yaml
- blueprints/README.md
- examples/sample_events.yaml

**Optional Removals** (8+ old doc files):
- DEPLOYMENT_CHECKLIST.md
- INSTALL_AND_TEST.md
- GITHUB_PUSH_GUIDE.md
- INDEX.md
- README_DEVELOPERS.md
- CHANGELOG.md
- PUSH_COMPLETE.md
- PUSH_TO_GITHUB_NOW.txt

**What Stays**:
- All v2 documentation
- Custom component files
- New installation guides

---

**Ready to cleanup?** Choose Option A or B above and run the commands!

---

**Version**: 2.0.0
**Date**: 2024-10-31

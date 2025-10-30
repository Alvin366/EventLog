# EventLog Deployment Checklist

Complete this checklist to deploy EventLog to your Home Assistant instance.

---

## Pre-Deployment (Do This First)

### Environment Check
- [ ] Home Assistant version is 2024.9.0 or later
  - Check: Settings → System → About
- [ ] You have access to `/config/` directory via terminal or file browser
- [ ] You have Valiug dashboard set up
- [ ] You have a working text editor for YAML files
- [ ] You have recent backup of Home Assistant configuration
  - Run: Settings → System → Backups → Create Backup

### Documentation Review
- [ ] Read `QUICK_START.md` (10 min read)
- [ ] Read `ARCHITECTURE.md` key sections (20 min read)
- [ ] Review `CONFIGURATION_GUIDE.md` completely (30 min read)
- [ ] Understand event structure and lifecycle (15 min read)

### Decision Making
- [ ] Decided: Deploy to test/production
- [ ] Decided: Who will do the deployment (user/agent)
- [ ] Decided: Timeline (when to deploy)
- [ ] Decided: How to handle issues (rollback plan)

---

## Step 1: Copy Custom Component

**Location**: Copy EventLogCollector to Home Assistant

```bash
# From your local clone/working directory:
cp -r custom_components/event_log_collector /config/custom_components/

# Verify:
ls -la /config/custom_components/event_log_collector/
```

**Files should exist**:
- [ ] `/config/custom_components/event_log_collector/__init__.py`
- [ ] `/config/custom_components/event_log_collector/manifest.json`

**Verify permissions**:
```bash
ls -la /config/custom_components/event_log_collector/*.py
# Should show: -rw-r--r-- (readable)
```

---

## Step 2: Create Helper Definitions

**Option A: Copy YAML Files** (Recommended)

```bash
# Copy helper definitions
cp config/input_text.yaml /config/
cp config/input_select.yaml /config/
cp config/input_boolean.yaml /config/
cp config/input_number.yaml /config/

# Verify:
ls -la /config/input_*.yaml
```

**Files should exist**:
- [ ] `/config/input_text.yaml`
- [ ] `/config/input_select.yaml`
- [ ] `/config/input_boolean.yaml`
- [ ] `/config/input_number.yaml`

**Option B: Create via UI** (If copying doesn't work)

1. [ ] Go to: Settings → Devices & Services → Helpers
2. [ ] Create each helper manually with names from config files
3. [ ] Set initial values as specified
4. [ ] Note: This takes longer but is more reliable

---

## Step 3: Update configuration.yaml

**Edit**: `/config/configuration.yaml`

**Add EventLogCollector section**:
```yaml
event_log_collector:
  - enabled: true
    log_file: /config/home-assistant.log
    scan_interval: 60
    categories:
      ERROR: major
      WARNING: warning
      CRITICAL: critical
```

**Add helper includes**:
```yaml
input_text: !include input_text.yaml
input_select: !include input_select.yaml
input_boolean: !include input_boolean.yaml
input_number: !include input_number.yaml
```

**Verify**:
- [ ] No YAML syntax errors
- [ ] Proper indentation (2 spaces)
- [ ] All files referenced exist

**Validate**:
```bash
# Check syntax (may not be available)
ha core check

# Or check via UI:
# Developer Tools → Check Configuration
```

---

## Step 4: Copy Scripts

**Copy event scripts**:
```bash
# Create scripts directory if needed
mkdir -p /config/scripts

# Copy scripts
cp scripts/*.yaml /config/scripts/

# Verify:
ls -la /config/scripts/
```

**Files should exist**:
- [ ] `/config/scripts/log_event.yaml`
- [ ] `/config/scripts/acknowledge_event.yaml`
- [ ] `/config/scripts/close_event.yaml`

**Add to configuration.yaml**:
```yaml
script: !include_dir_merge_named scripts/
```

---

## Step 5: Create Blueprint Automation

**Via Home Assistant UI**:

1. [ ] Go to: Settings → Automations & Scenes → Blueprints
2. [ ] Click "Import Blueprint"
3. [ ] Paste URL: `https://github.com/Alvin366/EventLog/blob/main/blueprints/event_logger.yaml`
4. [ ] Click "Import"
5. [ ] Click "Create Automation"
6. [ ] Configure:
   - [ ] Name: "EventLog Main Logger"
   - [ ] Collect HA Core Log Events: ON
   - [ ] Minimum Event Category: log
   - [ ] Enable Acknowledgment: ON
   - [ ] Enable Closure: ON
   - [ ] Enable Auto Archive: ON
7. [ ] Click "Create Automation"

**Verify automation created**:
- [ ] Automation appears in: Settings → Automations & Scenes → Automations
- [ ] Status shows: "Automation created"
- [ ] Check: Enabled toggle is ON

---

## Step 6: Add Dashboard Card

**Edit your Valiug dashboard YAML**:

1. [ ] Go to: Valiug dashboard
2. [ ] Click "Edit Dashboard"
3. [ ] Click "Add Card"
4. [ ] Choose: "Manual YAML"
5. [ ] Paste content from `lovelace/event_log_card.yaml`
6. [ ] Click "Save"
7. [ ] Verify card appears

**Alternative: Simple Entities Card**

If custom card doesn't work, use simple version:

```yaml
type: entities
title: "EventLog - Active Events"
entities:
  - entity: input_text.eventlog_active_events
    name: "Active Events"
  - entity: input_boolean.eventlog_enabled
    name: "EventLog Status"
  - entity: input_number.eventlog_archive_days
    name: "Archive After (days)"
```

---

## Step 7: Restart Home Assistant

**Via UI** (Safest method):

1. [ ] Go to: Settings → System
2. [ ] Click "Restart Home Assistant"
3. [ ] Wait for restart (2-5 minutes)
4. [ ] Check notification: "Home Assistant has restarted"

**Monitor restart**:
- [ ] Check logs: Settings → System → Logs
- [ ] Look for errors about event_log_collector
- [ ] Note any configuration issues

---

## Step 8: Verify Installation

### Check Component Loaded

**Via Developer Tools**:
1. [ ] Open: Developer Tools → States
2. [ ] Search: "event_log_collector"
3. [ ] Should show component in integrations
4. [ ] Should see entities starting with `input_`

**Via Logs**:
```bash
# Check for startup message
tail /config/home-assistant.log | grep -i "eventlog"

# Should see something like:
# "EventLogCollector started, monitoring: /config/home-assistant.log"
```

### Check Helpers Created

**Via UI**:
1. [ ] Go to: Settings → Devices & Services → Helpers
2. [ ] Search: "eventlog"
3. [ ] Should find:
   - [ ] `input_text.eventlog_active_events`
   - [ ] `input_text.eventlog_acknowledged_events`
   - [ ] `input_text.eventlog_archive`
   - [ ] `input_select.eventlog_category`
   - [ ] `input_boolean.eventlog_enabled`
   - [ ] `input_number.eventlog_archive_days`

### Check Automation Enabled

**Via UI**:
1. [ ] Go to: Settings → Automations & Scenes → Automations
2. [ ] Search: "EventLog"
3. [ ] Find: "EventLog Main Logger" automation
4. [ ] Status: Should show ENABLED (green toggle)
5. [ ] Trigger: Should show "event_log_collector.event_detected"

### Check Dashboard Card

**Via Dashboard**:
1. [ ] Navigate to Valiug dashboard
2. [ ] Find EventLog card section
3. [ ] Card displays without errors
4. [ ] Shows helper entities

---

## Step 9: Test Event Creation

### Manual Test via Service Call

**Via Developer Tools**:

1. [ ] Go to: Developer Tools → Services
2. [ ] Choose Service: `script.log_event`
3. [ ] Enter YAML:
```yaml
category: minor
source: test
title: Test Event
message: Testing EventLog system
recommended_action: No action needed
deduplication_key: test_event_001
```
4. [ ] Click "Call Service"

**Verify event created**:
- [ ] Check: Developer Tools → States
- [ ] Search: `input_text.eventlog_active_events`
- [ ] Value should contain JSON with your test event
- [ ] Check dashboard card - test event should appear

### Test Deduplication

**Create same event again**:

1. [ ] Repeat service call above with same `deduplication_key`
2. [ ] Check helper value updated
3. [ ] `occurrence_count` should be 2
4. [ ] `last_occurrence` timestamp should update
5. [ ] `first_occurrence` should stay the same

### Test Acknowledgment

**Via Script**:

1. [ ] From your test event, copy the `id` field
2. [ ] Call service: `script.acknowledge_event`
3. [ ] Enter:
```yaml
event_id: evt_xxxx_xxxxx_xxxx
note: "Testing acknowledgment"
```
4. [ ] Event should move to acknowledged list
5. [ ] Should disappear from active list

### Test Closure

**Via Script**:

1. [ ] Create new test event
2. [ ] Copy its event ID
3. [ ] Call service: `script.close_event`
4. [ ] Enter:
```yaml
event_id: evt_xxxx_xxxxx_xxxx
resolution_note: "Test resolved"
```
5. [ ] Event should move to archive
6. [ ] Should disappear from active list

---

## Step 10: Monitor for 24 Hours

### Daily Checks

**Each day for 7 days**:
- [ ] Check Home Assistant logs for errors
  - `tail /config/home-assistant.log | grep -i error`
- [ ] Monitor active events count
  - Check dashboard card
- [ ] Verify new log events are captured
  - Trigger an error/warning and check appears in EventLog
- [ ] Check helper state size
  - Developer Tools → States → Check character count

### Performance Monitoring

- [ ] Home Assistant CPU usage normal
- [ ] Home Assistant memory stable
- [ ] No "template rendering took" warnings
- [ ] No excessive automation errors
- [ ] Dashboard loads quickly

### Issues to Watch For

- [ ] EventLogCollector not appearing in integrations
- [ ] Events not being captured from logs
- [ ] Dashboard card not updating
- [ ] Helper storage growing too fast
- [ ] Duplicate event count too high

---

## Troubleshooting During Verification

### Component Not Found

**Problem**: EventLogCollector not appearing in integrations

**Solutions**:
```bash
# 1. Check file exists and has correct permissions
ls -la /config/custom_components/event_log_collector/

# 2. Check for syntax errors in Python
python3 -m py_compile /config/custom_components/event_log_collector/__init__.py

# 3. Check Home Assistant logs
tail -100 /config/home-assistant.log | grep -i "event_log_collector"

# 4. Restart Home Assistant again
```

### No Events Being Captured

**Problem**: Events not appearing in event log

**Solutions**:
1. Verify `eventlog_enabled` is ON
   - Check in Settings → Helpers → `input_boolean.eventlog_enabled`
2. Verify log file is readable
   - Run: `head /config/home-assistant.log`
3. Check automation is enabled
   - Settings → Automations → "EventLog Main Logger" should be ON
4. Manually trigger an event
   - Use service call (see Step 9)
5. Check event in helper state
   - Developer Tools → States → `input_text.eventlog_active_events`

### Dashboard Card Not Working

**Problem**: Card not displaying or showing errors

**Solutions**:
1. Clear browser cache
   - Ctrl+Shift+Delete → Clear cache → Refresh
2. Hard refresh dashboard
   - Ctrl+F5 or Cmd+Shift+R
3. Check entity exists
   - Developer Tools → States → Search "eventlog_active_events"
4. Check YAML syntax
   - Click "Edit Dashboard" → Review YAML
5. Try simple entities card instead
   - See Step 6 "Simple Entities Card" example

---

## Post-Deployment

### Document Your Setup

- [ ] Write down all helper entity IDs used
- [ ] Note EventLogCollector configuration
- [ ] Document any custom adjustments made
- [ ] Keep copy of your configuration.yaml changes

### Backup Configuration

```bash
# Create backup of working configuration
cp /config/configuration.yaml /config/configuration.yaml.eventlog_backup
cp -r /config/custom_components /config/custom_components.backup
```

### Plan Next Phase

- [ ] Decide on next event source (plant monitor, battery, etc.)
- [ ] Review ARCHITECTURE.md for Phase 2 planning
- [ ] Create GitHub issues for new features
- [ ] Schedule Phase 2 kickoff meeting

### Collect Feedback

- [ ] Note any issues or unexpected behavior
- [ ] Document what works well
- [ ] Gather feature requests
- [ ] Plan improvements for next phase

---

## Success Criteria

**MVP deployment is successful when**:

✅ EventLogCollector component loads without errors
✅ Helper entities all exist and have initial values
✅ Blueprint automation is created and enabled
✅ Dashboard card displays without errors
✅ Manual test event can be created via service call
✅ Deduplication works (occurrence_count increases)
✅ Acknowledgment moves event to acknowledged list
✅ Closure moves event to archive
✅ System runs stable for 24 hours
✅ No excessive errors in home-assistant.log

---

## Next Steps After Deployment

### If Everything Works:
1. Run system for 7 days
2. Monitor stability and performance
3. Adjust configuration if needed
4. Plan Phase 2 (additional event sources)
5. Begin development of event source blueprints

### If Issues Found:
1. Document the issue
2. Attempt troubleshooting from guide above
3. Check home-assistant.log for errors
4. Create GitHub issue with details
5. Rollback if needed using backup configuration

---

## Support Resources

- **QUICK_START.md** - Quick reference guide
- **CONFIGURATION_GUIDE.md** - Detailed setup
- **ARCHITECTURE.md** - How system works
- **README_DEVELOPERS.md** - Technical details
- **GitHub Issues**: https://github.com/Alvin366/EventLog/issues

---

**Deployment Checklist Version**: 0.1.0-MVP
**Last Updated**: 2024-10-30

---

## Deployment Status

- [ ] All checks completed
- [ ] Ready to deploy: YES / NO
- [ ] Deployment date: _______________
- [ ] Deployed by: _______________
- [ ] Issues found: YES / NO
- [ ] Issues resolved: YES / NO / N/A

**Sign-off**: _______________  Date: _______________

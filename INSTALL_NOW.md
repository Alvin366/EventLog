# EventLog v2.0.0 - Installation Steps

**Time Required**: 5 minutes
**Difficulty**: Easy
**Status**: Ready to Install

---

## Installation Steps (5 Minutes)

### Step 1: Open Terminal/SSH (1 minute)

Connect to your Home Assistant via SSH or terminal:

```bash
ssh root@192.168.1.xxx  # Or use your HA IP
# Or use Samba share to access /config
```

### Step 2: Navigate to Custom Components (1 minute)

```bash
cd /config/custom_components
```

Verify you're in the right place:
```bash
pwd
# Should output: /config/custom_components

ls
# Should show: eventlog, hacs, frigate, etc.
```

### Step 3: Clone from GitHub (1 minute)

Clone the EventLog repository to a temporary folder:

```bash
git clone https://github.com/Alvin366/EventLog.git temp-repo
```

Expected output:
```
Cloning into 'temp-repo'...
remote: Enumerating objects... done.
Receiving objects: 100% (XX objects)...
```

### Step 4: Copy Component Files (1 minute)

Copy the component from the temporary folder:

```bash
cp -r temp-repo/custom_components/eventlog .
```

Remove the temporary folder:

```bash
rm -rf temp-repo
```

### Step 5: Verify Installation (1 minute)

Verify all 4 files are in place:

```bash
ls -la /config/custom_components/eventlog/
```

Should show:
```
-rw-r--r-- __init__.py      (10.8 KB)
-rw-r--r-- manifest.json    (424 B)
-rw-r--r-- services.yaml    (2.8 KB)
-rw-r--r-- README.md        (8.2 KB)
```

All 4 files present? ✅ **Move to Step 6**

### Step 6: Restart Home Assistant (2-3 minutes)

In Home Assistant UI:

1. **Settings** (left sidebar, gear icon)
2. **System** (scroll down)
3. **Restart Home Assistant** (top right button)
4. Confirm the restart
5. **Wait 2-3 minutes** for restart to complete

---

## Verification (Do This After Restart)

### Check 1: Verify Component Loaded

1. **Settings > System > Logs**
2. Search for: `EventLog v2`
3. Should see:
   ```
   EventLog v2.0.0-alpha starting - monitoring /config/home-assistant.log
   EventLog component setup complete
   ```

**If you see this** ✅ Component loaded successfully!

### Check 2: Verify Services Registered

In the same logs, look for:
```
Registered service: eventlog.log_event
Registered service: eventlog.query_events
Registered service: eventlog.acknowledge_event
Registered service: eventlog.close_event
```

**If you see all 4** ✅ Services registered successfully!

### Check 3: Verify Services Appear in UI

1. **Developer Tools** (left sidebar)
2. **Services** tab
3. Search for: `eventlog`
4. Should see 4 services in dropdown

**If you see them** ✅ Component fully installed!

---

## Troubleshooting

### Issue: Git Clone Failed

**Error**: `git: command not found` or connection error

**Solution**:
- Install git: `apt-get install git`
- Or use Method 2 below (manual download)

### Issue: Copy Command Failed

**Error**: `cp: command not found` or permission denied

**Solution 1**: Check you're in right directory
```bash
pwd  # Should show /config/custom_components
```

**Solution 2**: Fix permissions
```bash
chmod 755 /config/custom_components
```

### Issue: Component Won't Load

**Symptoms**: No startup message in logs

**Solution**:
1. Check logs for error message
2. Verify all 4 files exist:
   ```bash
   ls -la /config/custom_components/eventlog/
   ```
3. Check manifest.json is valid:
   ```bash
   python3 -m json.tool /config/custom_components/eventlog/manifest.json
   ```
4. Restart Home Assistant again

### Issue: Services Don't Appear

**Symptoms**: Services not in Developer Tools

**Solution**:
1. Verify component loaded (check logs)
2. Wait full 2-3 minutes for restart
3. Refresh browser page: `F5` or `Ctrl+R`
4. Check in Developer Tools > Services > refresh dropdown

---

## Success Checklist

✅ Step 1: Connected via SSH/terminal
✅ Step 2: In `/config/custom_components` directory
✅ Step 3: Cloned repository successfully
✅ Step 4: Copied component files
✅ Step 5: All 4 files present
✅ Step 6: Restarted Home Assistant
✅ Check 1: Component started (logs show startup message)
✅ Check 2: Services registered (logs show 4 registrations)
✅ Check 3: Services in UI (Developer Tools shows services)

**If all checkmarks**, your installation is complete! ✅

---

## After Installation

### Next: Test the Component (30 minutes)

Follow: **V2_READY_FOR_TESTING.md**

5 quick tests:
1. Fire test event
2. Check InfluxDB storage
3. Query via service
4. Test deduplication
5. Verify log parsing

### Then: Set Up Monitoring

- Create automations that fire events
- Build dashboard cards to query events
- Monitor log file parsing

---

## Quick Commands Reference

All installation in one copy-paste block:

```bash
cd /config/custom_components
git clone https://github.com/Alvin366/EventLog.git temp-repo
cp -r temp-repo/custom_components/eventlog .
rm -rf temp-repo
ls -la eventlog/
echo "✅ Installation complete! Now restart Home Assistant."
```

---

## Alternative: Manual Download

If git clone doesn't work:

1. Go to: https://github.com/Alvin366/EventLog/tree/main/custom_components/eventlog
2. Click each file and download:
   - `__init__.py`
   - `manifest.json`
   - `services.yaml`
   - `README.md`
3. Create folder: `/config/custom_components/eventlog/`
4. Upload 4 files to that folder
5. Restart Home Assistant
6. Verify (same checks as above)

---

## Still Having Issues?

Check these resources:

- **Installation Details**: `INSTALLATION_FROM_GITHUB.md`
- **How It Works**: `HOW_CUSTOM_COMPONENTS_WORK.md`
- **Full Reference**: `GITHUB_SETUP_COMPLETE.md`
- **Testing Guide**: `V2_READY_FOR_TESTING.md`

---

**Version**: 2.0.0-alpha
**Date**: 2024-10-31
**Status**: Ready to Install

🚀 **Ready? Start with Step 1 above!**

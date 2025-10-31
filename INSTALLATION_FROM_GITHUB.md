# EventLog v2 - Installation from GitHub

**Version**: 2.0.0-alpha
**Date**: 2024-10-31

There are **3 ways** to install a custom component in Home Assistant:

1. ✅ **HACS** (Easiest) - If component is registered
2. ✅ **Manual Download** - Direct GitHub clone/download
3. ⏳ **Git Submodule** - For developers

This guide covers all three approaches.

---

## Method 1: Via HACS (Recommended - Once Listed)

HACS is the easiest method, but the component needs to be registered in the HACS repository first.

### Prerequisites
- HACS already installed (you have it ✅)

### Steps

1. **Open Home Assistant**
   - Go to: **Settings → Devices & Services → HACS**

2. **Add Custom Repository**
   - Click the **⋮ (three dots)** in top right
   - Select **"Custom repositories"**

3. **Enter Repository Details**
   - URL: `https://github.com/Alvin366/EventLog`
   - Category: **Integration**
   - Click **"Create"**

4. **Search for EventLog**
   - Go back to HACS main page
   - Click **"Integrations"**
   - Search: `eventlog`
   - Should see: "EventLog - Event Collector & Storage"

5. **Install**
   - Click on EventLog
   - Click **"Download"**
   - Select version: `2.0.0-alpha`
   - Wait for download to complete

6. **Restart Home Assistant**
   - Settings > System > Restart Home Assistant
   - Wait 2-3 minutes

7. **Verify Installation**
   - Settings > System > Logs
   - Look for: `EventLog v2.0.0-alpha starting`

---

## Method 2: Manual Installation (Works Now)

This method works immediately without waiting for HACS registration.

### Option A: Using Git Clone

**Prerequisites**:
- SSH access to `/config` directory (you have it ✅)

**Steps**:

1. **Clone Repository**
   ```bash
   cd /config/custom_components
   git clone https://github.com/Alvin366/EventLog.git eventlog
   cd eventlog
   git checkout main
   ```

   Or to clone just the component:
   ```bash
   cd /config/custom_components
   git clone --sparse https://github.com/Alvin366/EventLog.git
   cd EventLog
   git sparse-checkout set custom_components/eventlog
   ```

2. **Copy Component Files**
   ```bash
   # If cloned entire repo
   cp -r EventLog/custom_components/eventlog /config/custom_components/

   # Verify
   ls -la /config/custom_components/eventlog/
   ```

3. **Restart Home Assistant**
   ```
   Settings > System > Restart Home Assistant
   ```

4. **Verify**
   - Check logs for startup message
   - Should see: `EventLog v2.0.0-alpha starting`

### Option B: Manual File Download

**Steps**:

1. **Create Component Directory**
   ```bash
   mkdir -p /config/custom_components/eventlog
   ```

2. **Download Files from GitHub**

   Download these 4 files from:
   `https://github.com/Alvin366/EventLog/tree/main/custom_components/eventlog`

   - `__init__.py`
   - `manifest.json`
   - `services.yaml`
   - `README.md`

3. **Upload to Home Assistant**
   - Use Samba share or SSH to upload to `/config/custom_components/eventlog/`

4. **Verify Files**
   ```bash
   ls -la /config/custom_components/eventlog/
   # Should show: __init__.py, manifest.json, services.yaml, README.md
   ```

5. **Restart Home Assistant**
   ```
   Settings > System > Restart Home Assistant
   ```

---

## Method 3: Using Git Submodule (For Developers)

Keep the component in sync with GitHub updates automatically.

### Prerequisites
- Git installed on Home Assistant
- SSH access

### Steps

1. **Initialize Submodule**
   ```bash
   cd /config
   git init  # If not already a git repo
   git submodule add https://github.com/Alvin366/EventLog.git eventlog-repo
   ```

2. **Link Component Files**
   ```bash
   ln -s /config/eventlog-repo/custom_components/eventlog /config/custom_components/eventlog
   ```

3. **Update Submodule**
   ```bash
   git submodule update --remote
   ```

4. **Restart Home Assistant**
   ```
   Settings > System > Restart Home Assistant
   ```

---

## Verification Checklist

### ✅ Files in Place
```bash
ls -la /config/custom_components/eventlog/
```

Should show:
- ✅ `__init__.py` (10.8 KB)
- ✅ `manifest.json` (424 B)
- ✅ `services.yaml` (2.8 KB)
- ✅ `README.md` (8.2 KB)

### ✅ Component Loads
1. Restart Home Assistant
2. Wait 2-3 minutes
3. Check logs: **Settings > System > Logs**
4. Look for: `EventLog v2.0.0-alpha starting`

### ✅ Services Registered
Check logs for:
```
Registered service: eventlog.log_event
Registered service: eventlog.query_events
Registered service: eventlog.acknowledge_event
Registered service: eventlog.close_event
```

### ✅ No Errors
Should NOT see:
```
Error loading custom component eventlog
Failed to import eventlog
ModuleNotFoundError
```

---

## Troubleshooting

### Component Not Loading

**Problem**: `Error loading custom component eventlog`

**Solution**:
1. Check file permissions:
   ```bash
   ls -la /config/custom_components/eventlog/
   # Should show: drwxr-xr-x (readable)
   ```

2. Check Python syntax:
   ```bash
   python3 -m py_compile /config/custom_components/eventlog/__init__.py
   # Should have no output (means OK)
   ```

3. Check manifest.json is valid:
   ```bash
   python3 -c "import json; json.load(open('/config/custom_components/eventlog/manifest.json'))"
   # Should have no output (means OK)
   ```

4. Restart Home Assistant:
   ```
   Settings > System > Restart Home Assistant
   ```

### Services Not Registering

**Problem**: Services don't appear in Developer Tools

**Solution**:
1. Check logs for errors during startup
2. Verify `__init__.py` is loading
3. Look for: "Registered service" messages
4. Restart HA if needed

### Permission Denied Error

**Problem**: `Permission denied` when accessing component files

**Solution**:
```bash
# Fix file permissions
chmod -R 755 /config/custom_components/eventlog/
chmod 644 /config/custom_components/eventlog/*.py
chmod 644 /config/custom_components/eventlog/*.json
chmod 644 /config/custom_components/eventlog/*.yaml
```

### ImportError or Missing Dependencies

**Problem**: `ModuleNotFoundError` or import errors

**Solution**:
- EventLog has **NO external dependencies** (only Python built-ins)
- If you get import errors, check:
  1. File names are correct
  2. All 4 files present
  3. Restart Home Assistant

---

## Recommended: Method 2A (Git Clone)

For your setup, I recommend **Method 2A (Git Clone)** because:

✅ **Easy to update** - Just run `git pull`
✅ **Keep in sync** - Get updates automatically
✅ **Works now** - Don't need HACS registration
✅ **Full control** - Easy to modify if needed

### Quick Command to Install Now

```bash
cd /config/custom_components
git clone https://github.com/Alvin366/EventLog.git temp-repo
cp -r temp-repo/custom_components/eventlog .
rm -rf temp-repo

# Verify
ls -la eventlog/

# Restart Home Assistant
# Settings > System > Restart Home Assistant
```

---

## Updating the Component

### If Using Git Clone
```bash
cd /config/custom_components/eventlog
git pull origin main
# Then restart Home Assistant
```

### If Using HACS
```
HACS > Integrations > EventLog > Menu > Check for updates
```

### If Using Manual Download
1. Download latest files from GitHub
2. Replace files in `/config/custom_components/eventlog/`
3. Restart Home Assistant

---

## GitHub Repository Structure

The repository is organized as follows:

```
https://github.com/Alvin366/EventLog/
├── custom_components/eventlog/    ← Copy THIS folder
│   ├── __init__.py
│   ├── manifest.json
│   ├── services.yaml
│   └── README.md
├── docs/
├── blueprints/
├── README.md
└── ...
```

---

## Installation Paths Comparison

| Method | Time | Dependencies | Updates | Difficulty |
|--------|------|---|---|---|
| **HACS** | N/A (Not yet) | HACS | Automatic | Very Easy |
| **Git Clone** | 2 min | Git | Manual (easy) | Easy |
| **Manual Download** | 5 min | None | Manual | Easy |
| **Git Submodule** | 5 min | Git | Automatic | Medium |

---

## Next Steps After Installation

1. **Restart Home Assistant**
2. **Verify startup message** in logs
3. **Test component** with test event
4. **Follow**: `V2_READY_FOR_TESTING.md` for testing procedure

---

## Support

**GitHub**: https://github.com/Alvin366/EventLog
**Issues**: https://github.com/Alvin366/EventLog/issues
**Discussions**: https://github.com/Alvin366/EventLog/discussions

---

**Version**: 2.0.0-alpha
**Date**: 2024-10-31
**Status**: Ready for Installation

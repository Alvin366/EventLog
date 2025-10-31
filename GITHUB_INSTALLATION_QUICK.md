# EventLog v2 - Quick GitHub Installation

**Time**: 5 minutes
**Method**: Git Clone (recommended)
**Status**: Ready to install

---

## Quick Install (5 minutes)

### Step 1: Clone the Repository
```bash
cd /config/custom_components
git clone https://github.com/Alvin366/EventLog.git temp-repo
```

### Step 2: Copy Component Files
```bash
cp -r temp-repo/custom_components/eventlog .
rm -rf temp-repo
```

### Step 3: Verify Files
```bash
ls -la /config/custom_components/eventlog/
```

Should see:
```
-rw-r--r-- __init__.py
-rw-r--r-- manifest.json
-rw-r--r-- services.yaml
-rw-r--r-- README.md
```

### Step 4: Restart Home Assistant
```
Settings > System > Restart Home Assistant
Wait 2-3 minutes
```

### Step 5: Verify Installation
```
Settings > System > Logs
```

Look for:
```
EventLog v2.0.0-alpha starting - monitoring /config/home-assistant.log
EventLog component setup complete
Registered service: eventlog.log_event
```

---

## That's It! ✅

Your component is now installed and running.

**Next**: Follow `V2_READY_FOR_TESTING.md` to test the component (5 steps, 30 minutes)

---

## Directory Structure After Installation

```
/config/
└── custom_components/
    ├── eventlog/              ← NEW (from GitHub)
    │   ├── __init__.py
    │   ├── manifest.json
    │   ├── services.yaml
    │   └── README.md
    ├── hacs/
    ├── frigate/
    └── ... (other components)
```

---

## Troubleshooting

### Files not found after clone?
```bash
ls -la /config/custom_components/temp-repo/custom_components/eventlog/
# If found, copy as shown in Step 2
```

### Permission denied?
```bash
chmod -R 755 /config/custom_components/eventlog/
```

### Component still not loading?
1. Check logs for errors
2. Verify all 4 files exist
3. Check manifest.json is valid:
   ```bash
   python3 -m json.tool /config/custom_components/eventlog/manifest.json
   ```

---

## Updating Later

```bash
cd /config/custom_components/eventlog
# Check for updates on GitHub and update when ready
```

Or manually download latest files and replace.

---

**Version**: 2.0.0-alpha
**Repository**: https://github.com/Alvin366/EventLog
**Status**: Ready to Install

---

**Ready? Start with Step 1 above!** 🚀

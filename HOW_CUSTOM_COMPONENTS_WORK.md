# How Custom Components Work in Home Assistant

**Purpose**: Understand how Home Assistant loads custom components from GitHub
**Audience**: Users who want to install EventLog or other custom components

---

## What is a Custom Component?

A **custom component** is a Python module that extends Home Assistant's functionality. Unlike built-in integrations, custom components are:

- Hosted on GitHub (or similar)
- Installed manually into `/config/custom_components/`
- Loaded automatically when Home Assistant starts
- Can be updated independently

---

## How Home Assistant Loads Components

### 1. Startup Process

When Home Assistant starts:

```
Home Assistant Starts
    ↓
Load all integrations (built-in from /config/)
    ↓
Load all custom components (from /config/custom_components/)
    ↓
For each component:
  └─ Read manifest.json
  └─ Import __init__.py
  └─ Run async_setup()
  └─ Register services
    ↓
Ready!
```

### 2. Component Discovery

Home Assistant looks in `/config/custom_components/` for:

```
/config/custom_components/
├── eventlog/              ← Found!
│   ├── manifest.json      ← Read first
│   ├── __init__.py        ← Import & execute
│   ├── services.yaml
│   └── README.md
├── other_component/       ← Also loaded
│   ├── manifest.json
│   └── __init__.py
```

### 3. Component Loading

For each component, Home Assistant:

1. **Reads** `manifest.json` for metadata
2. **Validates** requirements are met
3. **Imports** the module (`__init__.py`)
4. **Executes** `async_setup()` function
5. **Registers** services, entities, etc.

### 4. Service Registration

When `eventlog` loads:

```python
# From __init__.py
async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    # ... component initialization ...

    # Register services
    hass.services.async_register(DOMAIN, SERVICE_LOG_EVENT, handle_log_event)
    hass.services.async_register(DOMAIN, SERVICE_QUERY_EVENTS, handle_query_events)
    # ... etc ...

    return True
```

Result: Services appear in Developer Tools automatically!

---

## EventLog Component Structure

### Required Files

```
/config/custom_components/eventlog/
├── __init__.py              ← REQUIRED (main code)
├── manifest.json            ← REQUIRED (metadata)
├── services.yaml            ← Optional (service definitions)
└── README.md                ← Optional (documentation)
```

### What Each File Does

#### `manifest.json` (Required)
```json
{
  "manifest_version": 1,
  "domain": "eventlog",              ← Component ID
  "name": "EventLog",                ← Display name
  "version": "2.0.0-alpha",          ← Version
  "requirements": [],                ← Dependencies (none for EventLog)
  "min_ha_version": "2024.1.0",      ← Minimum HA version
  "documentation": "...",            ← GitHub link
  "issue_tracker": "..."             ← Bug reports link
}
```

Home Assistant **requires** this file to load the component.

#### `__init__.py` (Required)
```python
import homeassistant.core as ha

async def async_setup(hass: ha.HomeAssistant, config):
    """Set up the component."""
    # Initialize component
    # Start services
    # Create entities
    # etc.

    return True  # Success
```

This is the **main code file** that runs when component loads.

#### `services.yaml` (Optional)
Defines services that appear in Developer Tools:
```yaml
log_event:
  name: Log Event
  description: Fire a custom event
  fields:
    category:
      description: Event category
```

#### `README.md` (Optional)
Documentation shown in HACS when browsing the component.

---

## Installation Methods Explained

### Method 1: Manual Copy

1. **Download** files from GitHub
2. **Create** folder: `/config/custom_components/eventlog/`
3. **Copy** 4 files into folder
4. **Restart** Home Assistant
5. **HA loads** component automatically

```
GitHub
  ↓ (download files)
Your Computer
  ↓ (copy to HA)
/config/custom_components/eventlog/
  ↓ (HA loads on restart)
Component Active!
```

### Method 2: Git Clone

1. **Clone** repository to custom_components
2. **Copy** component subfolder
3. **Restart** Home Assistant
4. **HA loads** component automatically

```
GitHub
  ↓ (git clone)
/config/custom_components/temp/
  ↓ (copy eventlog subfolder)
/config/custom_components/eventlog/
  ↓ (HA loads on restart)
Component Active!
```

### Method 3: HACS

1. **Register** component in HACS repository
2. **Search** HACS for component
3. **Click Install** in HACS UI
4. **HACS downloads** automatically
5. **Restart** Home Assistant
6. **HA loads** component automatically

```
HACS UI
  ↓ (click install)
Download from GitHub
  ↓ (HACS handles this)
/config/custom_components/eventlog/
  ↓ (HA loads on restart)
Component Active!
```

---

## Component Lifecycle

### On Home Assistant Startup

```
┌─────────────────────────────────────┐
│ Home Assistant Starts               │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│ Load Built-in Integrations          │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│ Load Custom Components              │
│ (/config/custom_components/)        │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│ For Each Component:                 │
│ 1. Read manifest.json               │
│ 2. Import __init__.py               │
│ 3. Call async_setup()               │
│ 4. Register services                │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│ EventLog Component                  │
│ ✅ Services registered              │
│ ✅ Log monitoring started           │
│ ✅ Ready to use                     │
└─────────────────────────────────────┘
```

### Startup Messages

Home Assistant logs appear in **Settings > System > Logs**:

```
2024-10-31 22:15:00 INFO (MainThread) [homeassistant.loader]
  Loaded eventlog from custom_components.eventlog

2024-10-31 22:15:00 INFO (MainThread) [custom_components.eventlog]
  EventLog v2.0.0-alpha starting - monitoring /config/home-assistant.log

2024-10-31 22:15:00 INFO (MainThread) [custom_components.eventlog]
  EventLog component setup complete
```

---

## How Services Work

### Service Registration

When `eventlog` loads, it registers services:

```python
# In __init__.py
hass.services.async_register(
    DOMAIN,                    # "eventlog"
    SERVICE_LOG_EVENT,         # "log_event"
    handle_log_event           # Handler function
)
```

### Service Appears in UI

After registration, service appears in:

1. **Developer Tools > Services**
   - Domain: `eventlog`
   - Service: `log_event`

2. **Service YAML Documentation**
   - Parameters defined in `services.yaml`
   - Descriptions shown in UI

### Calling a Service

**Via UI** (Developer Tools):
```yaml
Service: eventlog.log_event
Data:
  category: test
  title: "Test Event"
```

**Via YAML** (Automation):
```yaml
action:
  - service: eventlog.log_event
    data:
      category: test
      title: "Test Event"
```

**Via Python** (inside component):
```python
await hass.services.async_call(
    "eventlog",
    "log_event",
    {"category": "test", "title": "Test"}
)
```

---

## File Structure Comparison

### Built-in Integration (Home Assistant)
```
/path/to/homeassistant/components/
└── hass_component/
    ├── __init__.py
    ├── manifest.json
    └── ... (other files)
```

### Custom Component (Your EventLog)
```
/config/custom_components/
└── eventlog/
    ├── __init__.py
    ├── manifest.json
    └── ... (other files)
```

**Same structure!** Home Assistant treats them identically.

---

## What Happens When...

### Component Fails to Load

If `__init__.py` has an error:

```
ERROR (MainThread) [custom_components.eventlog] Error setting up integration
Traceback (most recent call last):
  File "...", line X, in async_setup
    ^ Error details here
```

**Solution**: Check logs, fix error, restart.

### Manifest is Missing

If `manifest.json` doesn't exist:

```
WARNING (...) Manifest missing for custom_components.eventlog
```

**Solution**: Add `manifest.json` file.

### Service Call Fails

If service handler has an error:

```
ERROR (...) Error calling eventlog.log_event
```

**Solution**: Check logs for traceback, fix code, restart.

---

## Best Practices

✅ **DO**:
- Keep component files in `/config/custom_components/DOMAIN/`
- Use `manifest.json` for metadata
- Log startup messages for debugging
- Handle errors gracefully

❌ **DON'T**:
- Don't modify built-in Home Assistant components
- Don't put component in random directories
- Don't skip `manifest.json`
- Don't ignore error messages

---

## Updating a Custom Component

### From GitHub

1. **Navigate** to component folder
   ```bash
   cd /config/custom_components/eventlog
   ```

2. **Check for updates** (if using git)
   ```bash
   git fetch origin
   git log origin/main -1 --oneline
   ```

3. **Pull updates**
   ```bash
   git pull origin main
   ```

4. **Restart Home Assistant**
   ```
   Settings > System > Restart Home Assistant
   ```

### Manual Update

1. **Download** latest files from GitHub
2. **Replace** files in `/config/custom_components/eventlog/`
3. **Restart** Home Assistant

---

## Troubleshooting Custom Components

### Component Not Loading

1. **Check logs**
   ```
   Settings > System > Logs
   ```

2. **Verify files exist**
   ```bash
   ls -la /config/custom_components/eventlog/
   ```

3. **Check Python syntax**
   ```bash
   python3 -m py_compile /config/custom_components/eventlog/__init__.py
   ```

4. **Verify manifest.json**
   ```bash
   python3 -m json.tool /config/custom_components/eventlog/manifest.json
   ```

### Service Not Appearing

1. **Check component loaded** (should see startup message)
2. **Check services.yaml** exists
3. **Restart Home Assistant**
4. **Go to Developer Tools > Services > refresh**

### Permission Errors

1. **Check file permissions**
   ```bash
   ls -la /config/custom_components/eventlog/
   ```

2. **Fix if needed**
   ```bash
   chmod -R 755 /config/custom_components/eventlog/
   chmod 644 /config/custom_components/eventlog/*.py
   chmod 644 /config/custom_components/eventlog/*.json
   ```

---

## Summary

**Home Assistant custom components are**:
- ✅ Python modules in `/config/custom_components/`
- ✅ Loaded automatically on startup
- ✅ Must have `manifest.json` and `__init__.py`
- ✅ Can register services, entities, etc.
- ✅ Updated by replacing files or pulling from git

**To install EventLog**:
1. Clone/download from GitHub
2. Copy to `/config/custom_components/eventlog/`
3. Restart Home Assistant
4. Done! Component loads automatically

---

**Version**: 2.0.0-alpha
**Date**: 2024-10-31

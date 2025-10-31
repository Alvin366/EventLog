# EventLog - Home Assistant Blueprint

A simple, powerful **Home Assistant Blueprint** for collecting and managing events in your home automation system.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Status](https://img.shields.io/badge/status-MVP-green.svg)

## Overview

EventLog is a **single Home Assistant blueprint** you import to start logging events from anywhere in your system. No custom components, no complex setup—just import and go!

**Perfect for**:
- Monitoring system events and errors
- Tracking device status changes
- Creating custom alerts and notifications
- Building event dashboards
- Understanding what's happening in your home

## Features

✨ **Simple Installation**
- Import blueprint via "Import Blueprint" menu
- Create automation from template
- Done! Start logging events

🎯 **Event Management**
- Categorize events (critical, major, minor, warning, log)
- Prevent duplicates automatically
- Acknowledge events (mark as seen)
- Close and archive resolved events

📊 **Flexible Storage**
- Stores in Home Assistant helpers (no database needed)
- JSON-based event data
- Full event history available
- Easy to query and display

🔌 **Multiple Sources**
- Main EventLog blueprint for processing
- Event Source blueprint for custom triggers
- Works with any automation or sensor
- Connect multiple event sources

## Quick Start (5 minutes)

### Step 1: Create Text Helpers (2 minutes)

Before importing the blueprint, create three text helpers to store events:

1. Go to **Settings → Devices & Services → Helpers**
2. Click **"Create Helper" → "Text"**

**Create Helper 1**:
- **Name**: EventLog Active Events
- **Entity ID**: `eventlog_active_events`
- **Max length**: 2048
- **Initial value**: `[]`
- Click **"Create"**

**Create Helper 2**:
- **Name**: EventLog Acknowledged Events
- **Entity ID**: `eventlog_acknowledged_events`
- **Max length**: 2048
- **Initial value**: `[]`
- Click **"Create"**

**Create Helper 3**:
- **Name**: EventLog Archive
- **Entity ID**: `eventlog_archive`
- **Max length**: 2048
- **Initial value**: `[]`
- Click **"Create"**

### Step 2: Import Blueprint (1 minute)

1. Go to **Settings → Automations & Scenes → Blueprints**
2. Click **Import Blueprint**
3. Paste: `https://raw.githubusercontent.com/Alvin366/EventLog/main/blueprints/eventlog_master.yaml`
4. Click **Import**

### Step 3: Create Automation (1 minute)

1. Click **Create Automation** on the imported blueprint
2. Configure with defaults or customize:
   - **Event Category**: `system`
   - **Event Severity**: `minor`
   - **Dedup Window**: 5 (minutes)
   - **Other options**: Leave as defaults or customize
3. Click **Create**

### Step 4: View Events (1 minute)

Create a dashboard card to display events:

```yaml
type: entities
title: EventLog
entities:
  - entity: input_text.eventlog_active_events
  - entity: input_text.eventlog_acknowledged_events
  - entity: input_text.eventlog_archive
```

### Step 5 (Optional): Add Event Sources

Use the **Event Source** blueprint to automatically feed events:

1. Import: `https://raw.githubusercontent.com/Alvin366/EventLog/main/blueprints/eventlog_event_source.yaml`
2. Create automation pointing to any entity
3. Events automatically go to EventLog

## How It Works

### Main Blueprint (`eventlog_master.yaml`)

The core EventLog blueprint that:
- Listens for `eventlog.log_event` events
- Stores events in helpers with metadata
- Handles deduplication
- Manages acknowledgment and closure
- Auto-archives closed events
- Optionally sends notifications

**Configuration**:
- Event Category & Severity
- Deduplication window (time to merge duplicates)
- Enable acknowledgment/closure features
- Archive settings
- Notification options

### Event Source Blueprint (`eventlog_event_source.yaml`)

Optional companion blueprint to automatically send events:
- Monitor any entity state change
- Trigger on conditions (below/above threshold)
- Format event title and message
- Send to EventLog automatically

**Use cases**:
- Battery sensors → low battery alerts
- Motion sensors → motion events
- Temperature sensors → climate alerts
- Door sensors → access events
- Any custom states → any automation

## Data Structure

Events are stored as JSON in `input_text` helpers:

```json
{
  "id": "1730000000_5234",
  "category": "system",
  "severity": "minor",
  "title": "Event Title",
  "message": "Event description",
  "timestamp": "2024-10-30T16:00:00",
  "first_occurrence": "2024-10-30T16:00:00",
  "last_occurrence": "2024-10-30T16:05:00",
  "count": 3,
  "dedup_key": "unique_identifier",
  "status": "active"
}
```

**Stored in helpers**:
- `input_text.eventlog_active_events` - Currently active events
- `input_text.eventlog_acknowledged_events` - Acknowledged but not closed
- `input_text.eventlog_archive` - Closed/archived events

## Examples

### Log Custom Events

Fire events to EventLog manually:
```yaml
action:
  - event: eventlog.log_event
    event_data:
      category: system
      title: Database Connection Failed
      message: Unable to connect to database
      dedup_key: db_connection_failed
```

### Monitor Battery Levels

Create automation from Event Source blueprint:
```yaml
Entity to Monitor: sensor.kitchen_sensor_battery
Trigger Condition: below_value
Trigger Value: 20
Event Title: "Low Battery: {{ entity_id }}"
Event Category: devices
Event Severity: minor
```

### Dashboard Display

Simple display card:
```yaml
type: entities
title: EventLog
entities:
  - input_text.eventlog_active_events
  - input_text.eventlog_acknowledged_events
```

## Configuration Reference

### Main Blueprint Inputs

| Input | Default | Description |
|-------|---------|-------------|
| Event Category | system | Type/source of event |
| Event Severity | minor | critical, major, minor, warning, log |
| Dedup Window | 5 min | Time to merge duplicates |
| Acknowledgment | true | Allow marking as seen |
| Closure | true | Allow closing events |
| Archive Days | 7 days | Auto-archive old events |
| Notify Critical | false | Send notifications |
| Notification Service | notify.notify | Service for alerts |

### Event Source Blueprint Inputs

| Input | Description |
|-------|-------------|
| Entity to Monitor | Any sensor or binary_sensor |
| Trigger Condition | state_change, below_value, above_value |
| Trigger Value | For numeric conditions |
| Event Title | Template for title |
| Event Message | Template for message |
| Event Category | Organization category |
| Event Severity | Importance level |
| Dedup Key | Unique identifier |

## Contributing

Found a bug? Have a feature request?

1. Check [GitHub Issues](https://github.com/Alvin366/EventLog/issues)
2. Create new issue if not found
3. Include: blueprint version, Home Assistant version, steps to reproduce

## Support

- **Issues**: [GitHub Issues](https://github.com/Alvin366/EventLog/issues)
- **Discussion**: [GitHub Discussions](https://github.com/Alvin366/EventLog/discussions)

---

**Version**: 0.1.0-MVP
**Status**: Production Ready
**Last Updated**: 2024-10-30

**Ready to get started?** Import the blueprint and create an automation! 🚀

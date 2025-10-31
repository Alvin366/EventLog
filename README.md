# EventLog v2.0.0 - Home Assistant Event Collection System

A sophisticated **Custom Component** for Home Assistant that automatically monitors logs, tracks events, and stores them in InfluxDB for querying and analysis.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Status](https://img.shields.io/badge/status-v2.0.0--alpha-yellow.svg)
![Version](https://img.shields.io/badge/version-2.0.0--alpha-blue.svg)

## Overview

EventLog v2 is a **complete redesign** from the MVP blueprint approach. Instead of storing JSON in helpers, we now use a **Custom Component** with **InfluxDB backend** for reliable, scalable event storage and querying.

**Key Improvement**: Move from impractical helper-based storage to proper time-series database (InfluxDB)

**Perfect for**:
- Monitoring system events and errors
- Tracking device status changes
- Creating custom alerts and notifications
- Building event dashboards
- Understanding what's happening in your home

## Features

✨ **Automatic Log Monitoring**
- Continuously watches `/config/home-assistant.log`
- Captures ERROR, WARNING, CRITICAL events automatically
- No manual setup required
- Runs in background (async)

🎯 **Intelligent Event Processing**
- Auto-categorizes and enriches events
- Maps severity (ERROR→major, WARNING→warning)
- Automatic deduplication (5-minute window)
- Creates event timeline with first/last occurrence

📊 **InfluxDB Storage**
- Time-series database designed for event data
- Queryable via SQL
- Scalable to millions of events
- Indexed for fast filtering
- Retention policies for auto-cleanup

🔌 **Service API**
- `eventlog.log_event` - Manually fire custom events
- `eventlog.query_events` - Query events from InfluxDB
- `eventlog.acknowledge_event` - Mark as seen
- `eventlog.close_event` - Archive resolved events

## Quick Start (30 minutes)

### Step 1: Verify InfluxDB Configuration (5 min)

Make sure InfluxDB is configured in Home Assistant:

```yaml
# configuration.yaml
influxdb:
  host: localhost
  port: 8086
  database: homeassistant
  username: homeassistant
  password: your_password
```

### Step 2: Component Already Installed (5 min)

The EventLog component is located at:
```
/config/custom_components/eventlog/
```

Files:
- ✅ `__init__.py` - Main component
- ✅ `manifest.json` - Metadata
- ✅ `services.yaml` - Service definitions
- ✅ `README.md` - Documentation

### Step 3: Restart Home Assistant (10 min)

1. Go to **Settings → System → Restart Home Assistant**
2. Wait 2-3 minutes for restart to complete
3. Check logs for startup messages

### Step 4: Verify Component Loaded (5 min)

1. Go to **Settings → System → Logs**
2. Look for:
```
EventLog v2.0.0-alpha starting - monitoring /config/home-assistant.log
EventLog component setup complete
Registered service: eventlog.log_event
```

### Step 5: Test with Sample Event (5 min)

1. Go to **Developer Tools → Services**
2. Select **eventlog: Log Event**
3. Enter:
```yaml
category: test
severity: warning
title: "Test Event"
message: "Testing EventLog v2"
dedup_key: "test_001"
```
4. Click **"Call Service"**

**For Detailed Testing Guide**: See `V2_READY_FOR_TESTING.md`

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

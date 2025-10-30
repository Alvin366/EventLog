# EventLog Architecture

## System Overview

EventLog is a multi-layer event collection, processing, and display system for Home Assistant.

### Architecture Layers

```
┌─────────────────────────────────────────────────────────────┐
│                    Dashboard Layer                           │
│              (Valiug Event Log Card)                         │
│        - Display events with filtering/sorting              │
│        - Action buttons (acknowledge, close)                │
│        - Real-time updates via WebSocket                    │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                  Storage Layer                               │
│  ┌──────────────────┐        ┌──────────────────────┐       │
│  │ Home Assistant   │        │     InfluxDB         │       │
│  │  Helpers         │        │   (Analytics)        │       │
│  │ (input_text)     │        │                      │       │
│  └──────────────────┘        └──────────────────────┘       │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│               Processing Layer                               │
│  ┌──────────────────┐  ┌──────────────────────┐             │
│  │ Deduplication    │  │ Lifecycle Manager    │             │
│  │ - Check existing │  │ - Acknowledgment     │             │
│  │ - Update counts  │  │ - Closure            │             │
│  │ - Merge data     │  │ - Auto-archival      │             │
│  └──────────────────┘  └──────────────────────┘             │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│               Collection Layer                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │     EventLogCollector Custom Component              │   │
│  │  - Monitors HA Core logs                            │   │
│  │  - Extracts error/warning events                    │   │
│  │  - Categorizes by severity                          │   │
│  │  - Triggers event logger automation                 │   │
│  └──────────────────────────────────────────────────────┘   │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                Source Layer                                  │
│  ┌──────────────────────────────────────────────────────┐   │
│  │     Home Assistant Core Logs                         │   │
│  │  - /config/home-assistant.log                       │   │
│  │  - HA Core errors and warnings                      │   │
│  │  - Integration startup/shutdown                     │   │
│  └──────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. EventLogCollector Custom Component

**Location**: `custom_components/event_log_collector/`

**Purpose**: Monitor HA Core logs and extract events

**Functionality**:
- Tail home-assistant.log periodically
- Parse log entries for errors, warnings, critical events
- Categorize events by severity and source
- Create event objects with metadata
- Trigger automation with event data

**Configuration**:
```yaml
event_log_collector:
  log_file: /config/home-assistant.log
  scan_interval: 60  # seconds
  max_log_size: 10485760  # 10MB
  categories:
    ERROR: major
    WARNING: warning
    CRITICAL: critical
```

**Output**: Fires event `event_log_collector.event_detected` with event data

### 2. Event Logger Automation

**Location**: `automations/log_event_processor.yaml`

**Purpose**: Receive and process events from collector

**Flow**:
1. Trigger: Event detected from EventLogCollector
2. Validate: Check event has required fields
3. Categorize: Determine severity level
4. Deduplicate: Check for existing events
5. Store: Save to helpers or InfluxDB
6. Notify: Update dashboard via state change

### 3. Deduplication System

**Location**: `automations/deduplication.yaml`

**Dedup Key**: Unique identifier for event type
- Format: `{source}_{component}_{type}`
- Example: `ha_core_auth_login_failed`

**Window**: Configurable time period (default: 5 minutes)
- Events within window: Increment `occurrence_count`
- Update `last_occurrence` timestamp
- Keep `first_occurrence` unchanged

**Storage**: Track in input_text helpers with JSON structure

### 4. Lifecycle Manager

**Location**: `automations/lifecycle_manager.yaml`

**States**:
```
active ──[acknowledge]──> acknowledged ──[close]──> closed
  │                                                    ▲
  │                                                    │
  └─────────[auto-resolve]────────────────────────────┘
             (after timeout)
```

**Acknowledgment**:
- User confirms they've seen the event
- Removes from "new events" list
- Keeps in history

**Closure**:
- User confirms issue resolved or action taken
- Event marked as closed
- Ready for archival

**Auto-resolve**:
- Critical/major: Default timeout (configurable)
- Automatically closes if condition resolves
- Example: Battery event closes when battery recharged

### 5. Archive & Cleanup

**Location**: `automations/archive_cleaner.yaml`

**Process**:
1. Find closed events older than archive period
2. Move to archive storage (separate helpers)
3. Remove from active helpers
4. Send to InfluxDB for long-term storage

**Configuration**:
- Archive period: 1-90 days (default: 7 days)
- Cleanup frequency: Daily at 2 AM
- Archive compression: Optional

## Data Storage

### Helper Storage (Active Events)

```yaml
input_text:
  eventlog_active_events:
    # JSON array of active events
    # Max size: ~255 chars
    # Format: Compressed JSON or index-based

  eventlog_acknowledged_events:
    # Events acknowledged but not closed

  eventlog_archive:
    # Old closed events (optional)
```

**Event JSON Structure**:
```json
{
  "id": "evt_20241030_140000_abc123",
  "category": "major",
  "source": "ha_core",
  "status": "active",
  "timestamp": "2024-10-30T14:00:00Z",
  "first_occurrence": "2024-10-30T14:00:00Z",
  "last_occurrence": "2024-10-30T14:00:00Z",
  "occurrence_count": 1,
  "title": "Authentication failed",
  "message": "Failed login attempt from 192.168.1.100",
  "recommended_action": "Check if device is trying to log in",
  "deduplication_key": "ha_core_auth_failed_192_168_1_100"
}
```

### InfluxDB Storage (Analytics & History)

**Measurement**: `eventlog`

**Tags**:
- `category`: critical, major, minor, warning, log
- `source`: ha_core, custom
- `status`: active, acknowledged, closed

**Fields**:
- `title`: Event title
- `message`: Event description
- `count`: Occurrence count
- `duration`: Time from first to last occurrence

**Queries**:
```influx
# Events by category in last 24 hours
SELECT * FROM eventlog WHERE time > now() - 24h GROUP BY category

# Critical events still active
SELECT * FROM eventlog WHERE category = 'critical' AND status = 'active'

# Event timeline
SELECT * FROM eventlog WHERE dedup_key = 'xyz' ORDER BY time DESC
```

## Event Flow Example: Authentication Failure

```
1. HA Core detects failed login attempt
2. Writes to home-assistant.log:
   "2024-10-30 14:00:00 WARNING (MainThread) [homeassistant.auth]
    Failed login attempt from 192.168.1.100"

3. EventLogCollector monitors log file
4. Identifies WARNING level, auth context
5. Creates event object:
   {
     category: "major",
     source: "ha_core",
     title: "Authentication failed",
     message: "Failed login from 192.168.1.100",
     dedup_key: "ha_core_auth_failed_192_168_1_100"
   }

6. Fires automation trigger: event_log_collector.event_detected

7. Automation processes event:
   - Check if dedup_key exists
   - If exists: update occurrence_count, last_occurrence
   - If new: create new event entry
   - Store in input_text.eventlog_active_events

8. InfluxDB gets event via REST API

9. Dashboard updates via state change entity

10. User sees "Authentication failed" in EventLog card
11. User clicks "Acknowledge" button
12. Event status changes to "acknowledged"
13. Event persists in history
14. After 7 days: Archived to storage
```

## Message Flow Diagram

```
┌──────────────────┐
│  HA Core Logs    │
└────────┬─────────┘
         │ (tail -f)
         ▼
┌──────────────────────────────────┐
│  EventLogCollector               │
│  Parse → Categorize → Extract   │
└────────┬─────────────────────────┘
         │ (event_detected)
         ▼
┌──────────────────────────────────┐
│  Event Logger Automation         │
│  Validate → Route               │
└────────┬─────────────────────────┘
         │
    ┌────┴────┐
    ▼         ▼
   ┌────────────────────┐  ┌────────────────────┐
   │ Deduplication      │  │ Validation         │
   │ Check & Update     │  │                    │
   └────────┬───────────┘  └───────────┬────────┘
            │                          │
            └────────────┬─────────────┘
                         ▼
            ┌────────────────────────┐
            │ Lifecycle Manager      │
            │ Set Status             │
            └────────────┬───────────┘
                         │
            ┌────────────┴────────────┐
            ▼                         ▼
    ┌──────────────────┐  ┌──────────────────┐
    │ Helper Storage   │  │  InfluxDB        │
    │ (input_text)     │  │  (analytics)     │
    └────────┬─────────┘  └──────────────────┘
             │
             ▼
    ┌──────────────────┐
    │ Dashboard        │
    │ Valiug Card      │
    └──────────────────┘
```

## Configuration Points

### User-Configurable Settings

```yaml
# input_number helpers
eventlog_archive_days: 7          # Days before archival
eventlog_dedup_window: 300        # Seconds for dedup
eventlog_auto_resolve_timeout: 86400  # Seconds to auto-close

# input_boolean helpers
eventlog_enabled: true            # Enable/disable system
eventlog_show_closed: false       # Show closed events
eventlog_auto_archive: true       # Enable auto-archival

# input_select helpers
eventlog_min_level: "minor"       # Minimum category to show
eventlog_display_mode: "compact"  # compact or detailed
```

## Performance Considerations

### Log File Monitoring
- Scan interval: 60 seconds (configurable)
- Efficient tail implementation (avoid re-reading entire file)
- Max log size: 10MB (auto-rotate by HA)

### Helper Storage
- Input_text size limit: ~255 chars
- Need JSON compression or pagination
- Archive old events regularly

### InfluxDB Integration
- Batch writes for efficiency
- Retention policy for old data
- Separate bucket for events

## Future Extensions

### Event Sources (Phase 2+)
- Plant Monitor integration
- Battery status monitoring
- Device connectivity tracking
- Climate/temperature alerts
- Network monitoring
- Custom blueprints

### Advanced Features
- Event escalation rules
- Notification triggers
- Email/Slack integration
- Event statistics/reporting
- Event history export
- Custom event templates
- Event correlations

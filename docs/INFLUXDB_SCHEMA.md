# EventLog InfluxDB Schema Design

## Overview

EventLog v2 uses InfluxDB as the primary storage backend for events. This document describes the measurement structure, tags, fields, and query patterns.

---

## InfluxDB Concepts for EventLog

**Measurement**: `eventlog_events` (main event storage)

**Tags** (indexed, queryable, low cardinality):
- `category` - Event type: system, device, security, custom
- `severity` - Priority: critical, major, minor, warning, log
- `source` - Event origin: log_parser, entity_monitor, custom
- `status` - Current state: active, acknowledged, closed, archived

**Fields** (non-indexed, searchable, can be any type):
- `title` (string) - Event title/name
- `message` (string) - Event description
- `count` (integer) - Deduplication count
- `dedup_key` (string) - Unique identifier for deduplication
- `first_occurrence` (string) - ISO timestamp of first occurrence
- `last_occurrence` (string) - ISO timestamp of last occurrence
- `entity_id` (string) - Home Assistant entity (if applicable)
- `custom_data` (string) - JSON for additional data

---

## Measurement: eventlog_events

### Schema Definition

```
Measurement: eventlog_events
├── Tags (indexed):
│   ├── category = {system, device, security, custom}
│   ├── severity = {critical, major, minor, warning, log}
│   ├── source = {log_parser, entity_monitor, custom}
│   └── status = {active, acknowledged, closed, archived}
└── Fields (values):
    ├── title: string
    ├── message: string
    ├── count: integer
    ├── dedup_key: string
    ├── first_occurrence: string (ISO 8601)
    ├── last_occurrence: string (ISO 8601)
    ├── entity_id: string (optional)
    └── custom_data: string (JSON, optional)
```

### Example Event Entry

```json
{
  "measurement": "eventlog_events",
  "tags": {
    "category": "system",
    "severity": "critical",
    "source": "log_parser",
    "status": "active"
  },
  "time": 1730000000000000000,
  "fields": {
    "title": "Home Assistant Core Error",
    "message": "Database connection failed: Connection refused",
    "count": 1,
    "dedup_key": "ha_core_db_error_001",
    "first_occurrence": "2024-10-30T16:00:00+00:00",
    "last_occurrence": "2024-10-30T16:00:00+00:00",
    "entity_id": "",
    "custom_data": "{\"error_code\": \"CONNECTION_REFUSED\", \"line\": 1234}"
  }
}
```

---

## Query Examples

### Get All Active Critical Events

```sql
SELECT * FROM eventlog_events
WHERE status = 'active' AND severity = 'critical'
ORDER BY time DESC
```

### Get Events by Category (Last 24 Hours)

```sql
SELECT * FROM eventlog_events
WHERE category = 'system' AND time > now() - 24h
ORDER BY time DESC
```

### Count Events by Severity

```sql
SELECT COUNT(*) FROM eventlog_events
WHERE time > now() - 7d
GROUP BY severity
```

### Get Recent System Errors (Last Hour)

```sql
SELECT * FROM eventlog_events
WHERE category = 'system'
  AND severity IN ('critical', 'major')
  AND time > now() - 1h
ORDER BY time DESC
```

### Find Duplicate Events (High Count)

```sql
SELECT * FROM eventlog_events
WHERE count > 5 AND status = 'active'
ORDER BY count DESC
```

---

## Component Architecture

### Custom Component: eventlog

**Location**: `/config/custom_components/eventlog/`

**Responsibilities**:
1. Watch `/config/home-assistant.log` for events
2. Parse ERROR/WARNING/CRITICAL lines
3. Deduplicate based on `dedup_key`
4. Write events to InfluxDB
5. Provide service calls for queries

**Services**:
- `eventlog.log_event` - Manually fire event
- `eventlog.query_events` - Query events from InfluxDB
- `eventlog.acknowledge_event` - Mark event as acknowledged
- `eventlog.close_event` - Close resolved event

---

## Data Lifecycle

```
Event Created
    ↓
Parse & Enrich (add category, severity)
    ↓
Check for Duplicates (dedup_key)
    ├─ YES: Update count, last_occurrence
    └─ NO: Create new event
    ↓
Write to InfluxDB (status: active)
    ↓
User acknowledges? (status: acknowledged)
    ↓
User closes? (status: closed)
    ↓
Auto-archive after 7 days? (status: archived)
```

---

## Retention Policies (Recommended)

**InfluxDB Retention**:
- Active events: Keep indefinitely
- Acknowledged: 30 days
- Closed: 90 days
- Archived: 1 year

Configure in InfluxDB:
```sql
CREATE RETENTION POLICY "active_forever" ON "homeassistant" DURATION INF REPLICATION 1
CREATE RETENTION POLICY "archive_90d" ON "homeassistant" DURATION 90d REPLICATION 1
```

---

## Helper Entity for Dashboard Display

Instead of storing raw JSON, create a helper that shows summaries:

**Entity**: `input_text.eventlog_summary`

Updated by automation that queries InfluxDB:
```json
{
  "total_active": 5,
  "critical": 2,
  "major": 1,
  "minor": 2,
  "last_updated": "2024-10-30T16:05:00"
}
```

---

## Advantages of This Schema

✅ **Time-Series Optimized**: InfluxDB excels at timestamped data
✅ **Queryable**: Full SQL access to events
✅ **Scalable**: Can store millions of events efficiently
✅ **Indexed**: Fast queries on category, severity, source, status
✅ **Retention**: Automatic data cleanup
✅ **Deduplication**: Built-in via dedup_key
✅ **Aggregations**: Easy to create summaries and reports

---

## Next Steps

1. Implement custom component to parse logs
2. Add InfluxDB write integration
3. Create blueprints to query and display events
4. Build dashboard with event summary cards

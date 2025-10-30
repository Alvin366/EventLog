# EventLog Configuration Guide

## Installation Steps

### Step 1: Copy Files to Home Assistant

1. Copy `custom_components/event_log_collector/` to `/config/custom_components/`
2. Copy `blueprints/` to `/config/blueprints/`
3. Copy `automations/` to `/config/automations/` or add to `automations.yaml`
4. Copy `scripts/` to `/config/scripts/` or add to `scripts.yaml`
5. Copy `config/` files to corresponding config location

### Step 2: Create Helper Entities

Add to `configuration.yaml` or create via UI:

```yaml
input_text:
  eventlog_active_events:
    name: "EventLog Active Events"
    max: 1024
    initial: '[]'

  eventlog_acknowledged_events:
    name: "EventLog Acknowledged Events"
    max: 1024
    initial: '[]'

  eventlog_archive:
    name: "EventLog Archive"
    max: 1024
    initial: '[]'

input_select:
  eventlog_category:
    name: "Event Category"
    options:
      - critical
      - major
      - minor
      - warning
      - log
    initial: log

  eventlog_status:
    name: "Event Status"
    options:
      - active
      - acknowledged
      - closed
    initial: active

  eventlog_min_level:
    name: "Minimum Event Level to Display"
    options:
      - critical
      - major
      - minor
      - warning
      - log
    initial: log

input_boolean:
  eventlog_enabled:
    name: "EventLog Enabled"
    initial: true
    icon: mdi:checkbox-marked-circle

  eventlog_show_closed:
    name: "Show Closed Events"
    initial: false
    icon: mdi:file-document

  eventlog_auto_archive:
    name: "Auto Archive Old Events"
    initial: true
    icon: mdi:archive

input_number:
  eventlog_archive_days:
    name: "Archive After (days)"
    min: 1
    max: 90
    step: 1
    unit_of_measurement: "days"
    icon: mdi:calendar-range

  eventlog_dedup_window:
    name: "Deduplication Window (seconds)"
    min: 30
    max: 3600
    step: 30
    unit_of_measurement: "s"
    icon: mdi:timer

  eventlog_auto_resolve_timeout:
    name: "Auto Resolve Timeout (seconds)"
    min: 300
    max: 604800
    step: 300
    unit_of_measurement: "s"
    icon: mdi:timer-outline
```

### Step 3: Configure EventLogCollector

Add to `configuration.yaml`:

```yaml
event_log_collector:
  enabled: true
  log_file: /config/home-assistant.log
  scan_interval: 60  # Check for new events every 60 seconds
  max_log_size: 10485760  # 10MB

  # Event categorization rules
  categories:
    ERROR: major
    WARNING: warning
    CRITICAL: critical

  # Keywords to ignore
  ignore_keywords:
    - "DEBUG"
    - "Sending keepalive ping"
    - "No new data"
```

### Step 4: Install Event Logger Blueprint

1. Go to Home Assistant UI
2. Settings → Blueprints → Import Blueprint
3. Import from: `https://github.com/Alvin366/EventLog/blob/main/blueprints/event_logger.yaml`
4. Create automation from blueprint
5. Configure:
   - Event category (select from dropdown)
   - Enable acknowledgment
   - Enable closure
   - Archive period

### Step 5: Configure InfluxDB Integration

Optional but recommended for analytics.

#### 5.1 Install InfluxDB Add-on

1. Settings → Add-ons → Add-on Store
2. Search for "InfluxDB"
3. Install and configure:
   - Database name: `eventlog`
   - Admin token: (generate or use existing)

#### 5.2 Configure InfluxDB in Home Assistant

Add to `configuration.yaml`:

```yaml
influxdb:
  host: localhost
  port: 8086
  database: eventlog
  username: admin
  password: !secret influxdb_password
  max_retries: 3
  default_measurement: eventlog

  # Include only event log related data
  include:
    domains:
      - input_text
      - input_select
```

Or use REST integration:

```yaml
rest:
  - resource: http://localhost:8086/api/v2/write?org=home&bucket=eventlog
    method: POST
    scan_interval: 30
```

### Step 6: Add Dashboard Card to Valiug

Edit Valiug dashboard YAML and add EventLog card:

```yaml
cards:
  - type: custom:eventlog-card
    title: "System Events"
    entity: input_text.eventlog_active_events
    acknowledged_entity: input_text.eventlog_acknowledged_events

    # Display options
    columns:
      - title
      - category
      - first_occurrence
      - last_occurrence
      - occurrence_count
      - recommended_action

    # Filtering
    filter_by_category: true
    filter_by_status: true
    show_closed: false

    # Sorting
    sort_by: last_occurrence
    sort_order: descending

    # Display limit
    max_events: 50

    # Styling
    color_mapping:
      critical: "#d32f2f"
      major: "#f57c00"
      minor: "#fbc02d"
      warning: "#1976d2"
      log: "#616161"
```

### Step 7: Restart Home Assistant

1. Settings → System → Restart Home Assistant
2. Wait for restart to complete
3. Verify EventLogCollector shows in Settings → Devices & Services

## Configuration Options

### EventLogCollector Settings

```yaml
event_log_collector:
  # Enable/disable the integration
  enabled: true

  # Path to HA log file
  log_file: /config/home-assistant.log

  # How often to scan log file (seconds)
  scan_interval: 60

  # Maximum log file size before rotation
  max_log_size: 10485760

  # Event level to category mapping
  categories:
    ERROR: major
    WARNING: warning
    CRITICAL: critical

  # Keywords to ignore
  ignore_keywords:
    - "DEBUG"
    - "keepalive"

  # Keywords to escalate to critical
  critical_keywords:
    - "CRITICAL"
    - "fatal"
    - "panic"
```

### Event Logger Blueprint Options

When creating automation from blueprint:

1. **Event Category**
   - Select minimum severity to log
   - Options: critical, major, minor, warning, log

2. **Enable Acknowledgment**
   - Allow users to acknowledge events
   - Keep acknowledged events in history

3. **Enable Closure**
   - Allow users to close events
   - Closed events ready for archival

4. **Archive Period**
   - Days to keep closed events
   - Default: 7 days
   - Range: 1-90 days

### Helper Configuration

#### input_number Settings

```yaml
eventlog_archive_days:
  value: 7  # Archive closed events after 7 days

eventlog_dedup_window:
  value: 300  # 5 minutes - time window for deduplication

eventlog_auto_resolve_timeout:
  value: 86400  # 24 hours - auto-close timeout for events
```

#### input_boolean Settings

```yaml
eventlog_enabled:
  state: true  # Master switch to enable/disable

eventlog_show_closed:
  state: false  # Show/hide closed events in dashboard

eventlog_auto_archive:
  state: true  # Auto-archive closed events
```

## Verification Steps

### 1. Check EventLogCollector Installation

```bash
# Should exist
ls -la /config/custom_components/event_log_collector/

# Check Home Assistant logs
tail -f /config/home-assistant.log | grep eventlog
```

### 2. Verify Helpers Created

1. Settings → Devices & Services → Helpers
2. Confirm these exist:
   - `input_text.eventlog_active_events`
   - `input_text.eventlog_acknowledged_events`
   - `input_select.eventlog_category`
   - `input_boolean.eventlog_enabled`
   - `input_number.eventlog_archive_days`

### 3. Test Event Creation

Use Developer Tools → Services:

```yaml
service: script.log_event
data:
  category: "minor"
  source: "test"
  title: "Test Event"
  message: "This is a test event"
  recommended_action: "No action needed"
  deduplication_key: "test_event_001"
```

Check that:
1. Event appears in `input_text.eventlog_active_events`
2. Dashboard card shows the event
3. Timestamp updates correctly

### 4. Test Deduplication

Trigger the same event again within 5 minutes:

```yaml
service: script.log_event
data:
  category: "minor"
  source: "test"
  title: "Test Event"
  message: "This is a test event"
  recommended_action: "No action needed"
  deduplication_key: "test_event_001"
```

Check that:
1. `occurrence_count` increases to 2
2. `last_occurrence` updates
3. `first_occurrence` stays the same

### 5. Test Acknowledgment & Closure

1. Click "Acknowledge" on test event
2. Event moves to acknowledged list
3. Click "Close" on event
4. Event status changes to closed
5. Wait for archive period, event archives

## Troubleshooting

### EventLogCollector Not Appearing

1. Check `/config/home-assistant.log` for errors:
   ```bash
   grep "event_log_collector" /config/home-assistant.log
   ```

2. Verify file permissions:
   ```bash
   ls -la /config/custom_components/event_log_collector/
   ```

3. Restart Home Assistant:
   ```
   Settings → System → Restart Home Assistant
   ```

### Events Not Being Logged

1. Verify `eventlog_enabled` is `true`
2. Check log file is accessible:
   ```bash
   tail /config/home-assistant.log | head -20
   ```

3. Check automation is enabled:
   - Settings → Automations → Event Logger

4. Test manually:
   ```
   Developer Tools → Services → script.log_event
   ```

### Dashboard Card Not Showing Events

1. Verify entity `input_text.eventlog_active_events` has data:
   - Developer Tools → States
   - Search for eventlog_active_events

2. Clear browser cache and reload dashboard

3. Verify card configuration in dashboard YAML

### InfluxDB Not Recording Events

1. Check InfluxDB add-on is running:
   - Settings → Add-ons → InfluxDB → Logs

2. Verify Home Assistant can connect:
   ```bash
   curl -X GET "http://localhost:8086/ping"
   ```

3. Check REST integration is configured correctly

## Next Steps

1. Monitor events for 24 hours to ensure stability
2. Fine-tune `eventlog_dedup_window` if too many duplicates
3. Adjust `eventlog_archive_days` based on storage needs
4. Connect additional event sources (plant monitor, battery alerts, etc.)
5. Create custom event blueprints for your use cases
6. Set up notifications for critical/major events
7. Configure InfluxDB for analytics and historical reporting

## Support

For issues or questions:
- Check logs: `/config/home-assistant.log`
- GitHub Issues: https://github.com/Alvin366/EventLog/issues
- Review documentation in `docs/` directory

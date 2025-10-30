# EventLog Quick Start Guide

Get EventLog up and running in 10 minutes!

## Prerequisites

- Home Assistant 2024.9.0 or later
- Valiug dashboard setup
- Access to Home Assistant configuration files

## Installation (Step-by-Step)

### 1. Copy Custom Component (2 min)

```bash
# Copy EventLogCollector to custom_components
cp -r custom_components/event_log_collector /config/custom_components/
```

### 2. Add Configuration (2 min)

Add to `configuration.yaml`:

```yaml
# EventLogCollector
event_log_collector:
  - enabled: true
    log_file: /config/home-assistant.log
    scan_interval: 60
    categories:
      ERROR: major
      WARNING: warning
      CRITICAL: critical

# EventLog Helpers
input_text: !include config/input_text.yaml
input_select: !include config/input_select.yaml
input_boolean: !include config/input_boolean.yaml
input_number: !include config/input_number.yaml

# EventLog Scripts
script: !include scripts/log_event.yaml

# EventLog Automations
automation: !include automations/event_logger_automation.yaml
```

### 3. Create Blueprint Automation (2 min)

1. Go to: Settings → Automations & Scenes → Blueprints
2. Click "Create Automation"
3. Select blueprint: `blueprints/event_logger.yaml`
4. Configure:
   - Collect HA Core Logs: ON
   - Minimum Level: log
   - Enable Acknowledgment: ON
   - Enable Closure: ON
   - Enable Auto Archive: ON

### 4. Add Dashboard Card (2 min)

Edit your Valiug dashboard YAML and add:

```yaml
cards:
  - type: custom:layout-card
    layout_type: vertical
    cards:
      - type: heading
        heading: System Events

      - type: entities
        title: Active Events
        entities:
          - entity: input_text.eventlog_active_events
```

### 5. Restart Home Assistant (2 min)

1. Settings → System → Restart Home Assistant
2. Wait for restart
3. Check: Settings → Devices & Services → event_log_collector

## Verify Installation

### Check Component Loaded

Developer Tools → States → search `event_log_collector`

Should show in list of integrations.

### Test Event Creation

Developer Tools → Services:

```yaml
service: script.log_event
data:
  category: "minor"
  source: "test"
  title: "Test Event"
  message: "Testing EventLog system"
  recommended_action: "No action needed"
  deduplication_key: "test_event_001"
```

Check: `input_text.eventlog_active_events` should contain the event.

### View on Dashboard

Open Valiug dashboard → scroll to Events card → should see test event.

## What's Happening Now

1. **EventLogCollector** is monitoring `/config/home-assistant.log`
2. **Every 60 seconds** it checks for new ERROR/WARNING/CRITICAL entries
3. **Events are created** and stored in `input_text.eventlog_active_events`
4. **Dashboard updates** automatically when new events arrive
5. **User can acknowledge/close** events from dashboard

## Next Steps

1. Monitor for 24 hours - adjust `scan_interval` if needed
2. Check `/config/home-assistant.log` for any errors
3. Create custom event sources (plant monitor, battery, etc.)
4. Configure InfluxDB for long-term storage and analytics
5. Set up notifications for critical/major events

## Troubleshooting

### EventLogCollector Not Found

```bash
# Check component exists
ls -la /config/custom_components/event_log_collector/

# Check HA logs
tail /config/home-assistant.log | grep "event_log_collector"

# Restart HA
```

### No Events Appearing

1. Verify `eventlog_enabled` is ON
   - Developer Tools → States → `input_boolean.eventlog_enabled`

2. Check log file is readable
   - `tail /config/home-assistant.log | head -20`

3. Test manually via service call (see above)

### Dashboard Card Not Showing

1. Clear browser cache (Ctrl+Shift+Delete)
2. Hard refresh dashboard (Ctrl+F5)
3. Check entity exists: States → `input_text.eventlog_active_events`

## Configuration Files Explained

| File | Purpose |
|------|---------|
| `custom_components/event_log_collector/__init__.py` | Main component that monitors logs |
| `blueprints/event_logger.yaml` | Blueprint automation for processing events |
| `scripts/log_event.yaml` | Script to manually log events |
| `config/input_text.yaml` | Helper entities for event storage |
| `config/input_select.yaml` | Dropdown selectors for categories |
| `config/input_boolean.yaml` | Toggle switches for configuration |
| `config/input_number.yaml` | Numeric configuration values |
| `lovelace/event_log_card.yaml` | Dashboard card for display |

## Key Entities to Monitor

```
# Active events (main storage)
input_text.eventlog_active_events

# Events waiting for action
input_text.eventlog_acknowledged_events

# Archived/closed events
input_text.eventlog_archive

# Master enable/disable
input_boolean.eventlog_enabled

# Archive behavior
input_number.eventlog_archive_days  (default: 7)
input_number.eventlog_dedup_window  (default: 300 seconds)
```

## Support

- GitHub: https://github.com/Alvin366/EventLog
- Issues: https://github.com/Alvin366/EventLog/issues
- Documentation: See `docs/` directory

## What's Next?

After basic setup works:

1. **Phase 2**: Add Plant Monitor events
2. **Phase 3**: Add Battery status monitoring
3. **Phase 4**: InfluxDB integration for analytics
4. **Phase 5**: Custom event blueprints for your needs
5. **Phase 6**: Notification system (Slack, email, push)

Happy logging! 🎯

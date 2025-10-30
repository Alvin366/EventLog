# EventLog Configuration

Helper entity configurations for EventLog system.

## Files

### input_text.yaml
Text helpers for storing event data as JSON.

**Entities**:
- `eventlog_active_events` - Active events (max 2048 chars)
- `eventlog_acknowledged_events` - Acknowledged events (max 2048 chars)
- `eventlog_archive` - Archived/closed events (max 4096 chars)
- `eventlog_influxdb_url` - InfluxDB API endpoint
- `eventlog_influxdb_user` - InfluxDB username
- `eventlog_influxdb_password` - InfluxDB password

### input_select.yaml
Dropdown selection helpers for configuration.

**Entities**:
- `eventlog_category` - Event category selector
- `eventlog_status` - Event status selector
- `eventlog_min_level` - Minimum display level filter
- `eventlog_display_mode` - Compact/detailed display mode
- `eventlog_sort_by` - Sort events by field

### input_boolean.yaml
Toggle switches for feature configuration.

**Entities**:
- `eventlog_enabled` - Master enable/disable
- `eventlog_show_closed` - Show/hide closed events
- `eventlog_auto_archive` - Enable auto-archival
- `eventlog_enable_influxdb` - Enable InfluxDB integration
- `eventlog_show_active_only` - Filter to active only
- `eventlog_enable_notifications` - Enable notifications

### input_number.yaml
Numeric configuration values.

**Entities**:
- `eventlog_archive_days` - Archive after N days (1-90, default: 7)
- `eventlog_dedup_window` - Dedup window seconds (30-3600, default: 300)
- `eventlog_auto_resolve_timeout` - Auto-close timeout (300-604800, default: 86400)
- `eventlog_max_events` - Maximum events to keep (10-1000, default: 100)
- `eventlog_scan_interval` - Log scan interval seconds (10-300, default: 60)

## Installation

Add to `configuration.yaml`:

```yaml
input_text: !include config/input_text.yaml
input_select: !include config/input_select.yaml
input_boolean: !include config/input_boolean.yaml
input_number: !include config/input_number.yaml
```

Or create helpers via Home Assistant UI:
1. Settings → Devices & Services → Helpers
2. Create each helper manually with same names

## Configuration

### Key Settings

#### Archive Period
- **Entity**: `input_number.eventlog_archive_days`
- **Default**: 7 days
- **Range**: 1-90 days
- **Effect**: Closed events automatically archived after this period

#### Deduplication Window
- **Entity**: `input_number.eventlog_dedup_window`
- **Default**: 300 seconds (5 minutes)
- **Range**: 30-3600 seconds
- **Effect**: Events with same dedup_key within window are merged

#### Auto-Resolve Timeout
- **Entity**: `input_number.eventlog_auto_resolve_timeout`
- **Default**: 86400 seconds (24 hours)
- **Range**: 300-604800 seconds
- **Effect**: Events automatically closed after this period

#### Minimum Display Level
- **Entity**: `input_select.eventlog_min_level`
- **Options**: critical, major, minor, warning, log
- **Default**: log (show all)
- **Effect**: Only show events at or above this severity

#### Display Mode
- **Entity**: `input_select.eventlog_display_mode`
- **Options**: compact, detailed, minimal
- **Effect**: Changes dashboard event display format

## Customization

### Adding Custom Helpers

To add more configuration options:

1. Create helper in YAML file
2. Add to configuration.yaml includes
3. Update automations/scripts to use new helper
4. Add to dashboard for user control

**Example**:
```yaml
# config/input_text.yaml
eventlog_notification_channels:
  name: "Notification Channels"
  icon: mdi:message
  max: 255
  initial: "email,slack"
```

### Adjusting Limits

To allow more events to be stored:

1. Increase `input_text` max value
2. Implement pagination in scripts
3. Use InfluxDB for overflow storage
4. Archive more frequently

**Example**:
```yaml
eventlog_active_events:
  name: "EventLog Active Events"
  max: 4096  # Increase from 2048
```

## Size Limitations

### Input Text Limits
- Maximum 255 characters per line (some HA versions)
- Typical limit: 2048-4096 characters total
- JSON overhead reduces practical event count

**Approximate Event Capacity**:
- Per helper: 20-50 events (depending on detail)
- Compact format (minimal fields): 50+ events
- Detailed format (all fields): 15-20 events

**Solutions**:
1. Decrease `eventlog_archive_days` to archive more quickly
2. Increase `eventlog_max_events` and implement cleanup
3. Use InfluxDB for additional storage
4. Implement pagination system

## Backup & Restore

### Backup Helpers
Helpers are stored in Home Assistant's database. Backup via:

```bash
# Standard Home Assistant backup
# Settings → System → Backups → Create Backup

# Manual JSON export
# Developer Tools → States → export entity states
```

### Restore Helpers
1. Restore Home Assistant backup, or
2. Manually restore states:
   - Developer Tools → States → Set State
   - Paste previously exported JSON

## Troubleshooting

### Helper Not Appearing
1. Check YAML syntax
2. Verify includes in configuration.yaml
3. Check Home Assistant logs for errors
4. Restart Home Assistant

### Helper State Not Updating
1. Verify automation is enabled
2. Check script calls are working
3. Look for JSON parse errors in logs
4. Test script manually via Developer Tools

### Storage Full
1. Archive old events more frequently
2. Lower `eventlog_max_events`
3. Implement cleanup automation
4. Migrate to InfluxDB

## Performance Notes

- Helper updates are fast (< 100ms)
- State changes trigger automations
- Large JSON causes slight delay
- Recommend max 50 active events per helper

## Future Improvements

- Custom helper categories
- Dynamic helper creation
- Helper compression
- Distributed storage
- Database backend

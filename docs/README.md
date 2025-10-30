# EventLog Documentation

Complete documentation for the EventLog event collection and management system.

## Quick Links

- **Getting Started**: [CONFIGURATION_GUIDE.md](CONFIGURATION_GUIDE.md)
- **System Design**: [ARCHITECTURE.md](ARCHITECTURE.md)
- **Event Catalog**: [EVENT_SOURCES.md](EVENT_SOURCES.md)
- **Development**: [DEVELOPMENT.md](../README_DEVELOPERS.md)

## Documentation Files

### ARCHITECTURE.md
Complete system architecture and design documentation.

**Covers**:
- System overview and layers
- Component details (EventLogCollector, automation, deduplication)
- Event lifecycle and state transitions
- Data storage (helpers and InfluxDB)
- Message flow diagrams
- Performance considerations

**Read this if**: You want to understand how EventLog works internally

### CONFIGURATION_GUIDE.md
Step-by-step installation and configuration guide.

**Covers**:
- Installation steps (7 total)
- Helper creation
- EventLogCollector configuration
- Blueprint setup
- Dashboard integration
- InfluxDB optional setup
- Verification steps
- Troubleshooting common issues

**Read this if**: You're installing EventLog for the first time

### EVENT_SOURCES.md
Map of available event sources and how to integrate them.

**Covers**:
- Home Assistant Core log events
- Plant Monitor integration
- Battery monitoring
- Device status events
- Custom event sources
- Future planned sources

**Read this if**: You want to add new event sources

### DEVELOPMENT.md
Developer guide for extending EventLog.

**Covers**:
- Development setup
- Component structure
- Creating custom blueprints
- Contributing guidelines
- Testing strategies

**Read this if**: You want to extend or modify EventLog

## Main Documentation (Root Level)

### README.md
Project overview and feature summary.

### QUICK_START.md
Get EventLog running in 10 minutes.

### CHANGELOG.md
Version history and release notes.

### README_DEVELOPERS.md
Developer contribution guide.

## Feature Documentation

### Event Categories
Events are categorized by severity:

| Category | Severity | Examples | Typical Actions |
|----------|----------|----------|-----------------|
| **critical** | Highest | System access attempts, auth failures | Alert user, require acknowledgment |
| **major** | High | Device offline, component failure | Notify user, recommend action |
| **minor** | Medium | Low battery, watering needed | Log and display |
| **warning** | Low | Temperature alert, usage threshold | Log for reference |
| **log** | Lowest | Info messages, routine events | Archive and analyze |

### Event Lifecycle
```
active → [acknowledged] → [closed] → archived
  ↓                                      ↑
  └──── auto-resolve (timeout) ─────────┘
```

## Configuration Reference

### Essential Entities

```yaml
# Master controls
input_boolean.eventlog_enabled              # Enable/disable system

# Storage
input_text.eventlog_active_events           # Current events
input_text.eventlog_acknowledged_events     # Acknowledged but not closed
input_text.eventlog_archive                 # Closed/archived events

# Configuration
input_number.eventlog_archive_days          # Days before archival (1-90)
input_number.eventlog_dedup_window          # Dedup time window (30-3600 sec)
input_select.eventlog_min_level             # Minimum level to show
input_boolean.eventlog_show_closed          # Show closed events
input_boolean.eventlog_auto_archive         # Enable auto-archival
```

## Common Tasks

### View Active Events
1. Developer Tools → States
2. Search: `input_text.eventlog_active_events`
3. View state value (JSON array)

### Create Custom Event
```yaml
service: script.log_event
data:
  category: "minor"
  source: "custom"
  title: "Event Title"
  message: "Detailed message"
  recommended_action: "What to do"
  deduplication_key: "unique_key"
```

### Acknowledge Event
```yaml
service: script.acknowledge_event
data:
  event_id: "evt_20241030_140000_abc123"
  note: "Investigating this"
```

### Close Event
```yaml
service: script.close_event
data:
  event_id: "evt_20241030_140000_abc123"
  resolution_note: "Issue resolved"
```

### Filter Events
Use `input_select.eventlog_min_level` to show only events at or above selected severity.

### Check Statistics
Dashboard card shows:
- Total active events
- Events by category (critical, major, minor, etc.)
- Last update time
- Status breakdown

## API Reference

### Services

#### script.log_event
Create a new event entry.

**Parameters**:
- `category` (string, required): critical|major|minor|warning|log
- `source` (string, required): Event source identifier
- `title` (string, required): Short title
- `message` (string, required): Detailed message
- `recommended_action` (string, optional): Suggested action
- `deduplication_key` (string, optional): Dedup identifier

#### script.acknowledge_event
Acknowledge an active event.

**Parameters**:
- `event_id` (string, required): Event ID to acknowledge
- `note` (string, optional): Acknowledgment note

#### script.close_event
Close a resolved event.

**Parameters**:
- `event_id` (string, required): Event ID to close
- `resolution_note` (string, optional): How it was resolved

### Events

#### event_log_collector.event_detected
Fired when EventLogCollector detects a new log event.

**Data**:
- `timestamp`: When event occurred
- `category`: Severity level
- `source`: ha_core
- `title`: Event title
- `message`: Event details
- `recommended_action`: Suggested fix
- `deduplication_key`: Dedup identifier

## Troubleshooting

### Events Not Being Logged
1. Check `eventlog_enabled` is ON
2. Verify log file is readable: `tail /config/home-assistant.log`
3. Check automation is enabled: Settings → Automations
4. Review HA logs for errors

### Dashboard Not Updating
1. Clear browser cache (Ctrl+Shift+Delete)
2. Hard refresh (Ctrl+F5)
3. Check entity exists in States
4. Verify card configuration in dashboard YAML

### Too Many Events
1. Lower `eventlog_archive_days` to archive faster
2. Increase `eventlog_dedup_window` to merge more events
3. Lower `eventlog_min_level` to filter out less important ones
4. Implement cleanup automation

### Storage Full
See config/README.md for size limitations and solutions

## Advanced Topics

### InfluxDB Integration
Optional integration for long-term storage and analytics.

See CONFIGURATION_GUIDE.md → "Configure InfluxDB Integration"

### Custom Blueprints
Create blueprints for new event sources.

See blueprints/README.md for examples

### Event Deduplication
How duplicate events are merged and managed.

See ARCHITECTURE.md → "Deduplication System"

### Performance Tuning
Optimize for your Home Assistant instance.

See ARCHITECTURE.md → "Performance Considerations"

## FAQ

**Q: How long are events kept?**
A: Closed events are archived after 7 days by default. Edit `eventlog_archive_days` to change.

**Q: Can I delete events?**
A: Closed events are archived (stored separately). To delete, manually edit the helper via Developer Tools.

**Q: How many events can EventLog handle?**
A: About 20-50 active events depending on detail level. Use archival and InfluxDB for more.

**Q: Does EventLog persist across restarts?**
A: Yes, events are stored in Home Assistant helpers which are persistent.

**Q: Can I export event history?**
A: Via InfluxDB if enabled. Otherwise, manually export helper states via Developer Tools.

**Q: How do I integrate custom event sources?**
A: Create a blueprint that calls `script.log_event`. See blueprints/README.md for examples.

## Getting Help

- **Bug Reports**: GitHub Issues with logs and reproduction steps
- **Feature Requests**: GitHub Discussions with use case
- **General Questions**: GitHub Discussions or HA Forums
- **Documentation Issues**: GitHub Issues with what needs clarification

## Community

- GitHub: https://github.com/Alvin366/EventLog
- Home Assistant Forums: https://community.home-assistant.io/
- HA Blueprint Community: https://www.home-assistant.io/blueprints/

## Contributing

See README_DEVELOPERS.md for contribution guidelines.

## License

MIT License - See LICENSE file

---

**Last Updated**: 2024-10-30
**Documentation Version**: 0.1.0-MVP

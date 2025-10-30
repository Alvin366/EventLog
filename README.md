# EventLog - Home Assistant Event Collector & Dashboard

A configurable event collection and display system for Home Assistant that aggregates events from various sources and displays them in a unified dashboard interface.

## Overview

EventLog is a comprehensive event management solution that:
- Collects Home Assistant Core logs and system events
- Categorizes events (critical, major, minor, warning, log)
- Manages event lifecycle (creation, acknowledgment, closure, archival)
- Displays events in a configurable Valiug dashboard
- Stores events in Home Assistant helpers and InfluxDB
- Prevents duplicate event entries
- Auto-archives events after configurable periods

## Features

### Core Functionality
- **Event Aggregation**: Centralized collection of events from HA Core logs
- **Event Categorization**: Automatic categorization by severity level
- **Lifecycle Management**: Track event status from creation to closure
- **Deduplication**: Prevent duplicate entries with configurable dedup windows
- **Dashboard Integration**: Display events in Valiug dashboard with filtering
- **Archival System**: Auto-archive closed events after configurable period
- **Action Buttons**: Acknowledge and close critical/major events

### Event Categories
- **Critical**: System access attempts, critical failures
- **Major**: Network issues, component failures, temperature alerts
- **Minor**: Battery low, device status changes, maintenance reminders
- **Warning**: Non-critical alerts, threshold warnings
- **Log**: Information and system events

## Quick Start

### Installation

1. Copy files to Home Assistant configuration directory
2. Add EventLog configuration to `configuration.yaml`
3. Create helpers (input_text, input_select)
4. Install event logger blueprint
5. Configure event sources in InfluxDB
6. Add dashboard card to Valiug

### Configuration

See [CONFIGURATION_GUIDE.md](docs/CONFIGURATION_GUIDE.md) for detailed setup instructions.

## Architecture

### Project Structure

```
EventLog/
├── blueprints/
│   └── event_logger.yaml          # Main event logger blueprint
├── automations/
│   ├── log_event_processor.yaml   # Routes and processes events
│   ├── deduplication.yaml         # Prevents duplicates
│   ├── lifecycle_manager.yaml     # Handles acknowledgment/closure
│   └── archive_cleaner.yaml       # Archives old events
├── custom_components/
│   └── event_log_collector/       # EventLogCollector component
├── config/
│   ├── input_select.yaml          # Category/status selectors
│   ├── input_boolean.yaml         # Configuration toggles
│   └── input_number.yaml          # Configuration values
├── lovelace/
│   └── event_log_card.yaml        # Dashboard card definition
├── scripts/
│   ├── log_event.yaml             # Add event script
│   ├── acknowledge_event.yaml     # Acknowledge script
│   ├── close_event.yaml           # Close event script
│   └── cleanup_events.yaml        # Archive script
└── docs/
    ├── ARCHITECTURE.md
    ├── CONFIGURATION_GUIDE.md
    ├── EVENT_SOURCES.md
    └── DEVELOPMENT.md
```

### Data Flow

```
HA Core Logs → EventLogCollector → Deduplication → Helper Storage → Dashboard
                                                  → InfluxDB → Analytics
```

### Event Data Structure

```yaml
event:
  id: "unique_id"
  category: "critical|major|minor|warning|log"
  source: "ha_core|custom"
  status: "active|acknowledged|closed"
  timestamp: "2024-10-30T14:00:00Z"
  first_occurrence: "2024-10-30T14:00:00Z"
  last_occurrence: "2024-10-30T14:30:00Z"
  occurrence_count: 3
  title: "Event title"
  message: "Detailed event message"
  recommended_action: "Suggested action"
  deduplication_key: "unique_key"
```

## Event Sources

### Phase 1 (MVP)
- Home Assistant Core logs (errors, warnings, critical)
- System health events
- Component startup/shutdown events

### Future Phases
- Plant Monitor integration (watering status)
- Battery status from ZHA/Zigbee2MQTT
- Device status changes
- Custom event sources via blueprints
- Climate alerts
- Network monitoring

## Configuration

### Home Assistant Helpers

The system requires these helpers to be created:

```yaml
# input_select for event categories
input_select:
  eventlog_category:
    options:
      - critical
      - major
      - minor
      - warning
      - log

# input_select for event status
input_select:
  eventlog_status:
    options:
      - active
      - acknowledged
      - closed

# input_number for archive period (days)
input_number:
  eventlog_archive_days:
    min: 1
    max: 90
    unit_of_measurement: "days"
    value: 7
```

## Development

### Agents

- **Planning Agent**: Project planning and requirements
- **Design Agent**: Architecture and UI/UX design
- **Development Agent**: Implementation and coding
- **Testing Agent**: Quality assurance and validation

### Workflow

Events are processed through:
1. **Collection**: HA logs captured via EventLogCollector
2. **Processing**: Automation routes to appropriate handlers
3. **Deduplication**: Check for existing events
4. **Storage**: Save to helpers and InfluxDB
5. **Display**: Render in dashboard
6. **Maintenance**: Archive old events

## Usage Examples

### Adding a Custom Event

Events can be logged via script or automation:

```yaml
service: script.log_event
data:
  category: "major"
  source: "custom"
  title: "Device Connection Lost"
  message: "WiFi device has been offline for 30 minutes"
  recommended_action: "Check device power and WiFi connection"
  deduplication_key: "device_offline_kitchen_sensor"
```

### Filtering Events

Dashboard supports filtering by:
- Category (critical, major, minor, warning, log)
- Status (active, acknowledged, closed)
- Source (ha_core, custom)
- Time range (last hour, day, week)

## Dashboard Integration

The Valiug dashboard includes an EventLog card showing:
- Event title and category badge
- Time since first occurrence and last update
- Event count (for duplicate events)
- Recommended action
- Action buttons (acknowledge, close for critical/major)
- Status indicator

## Contributing

See [DEVELOPMENT.md](docs/DEVELOPMENT.md) for development guidelines.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history.

## License

MIT License - See [LICENSE](LICENSE) for details

## Support

For issues and questions:
- GitHub Issues: https://github.com/Alvin366/EventLog/issues
- Documentation: See docs/ directory

## Version

Current: 0.1.0-MVP (Home Assistant Core logs integration)

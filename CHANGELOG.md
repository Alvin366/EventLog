# Changelog

All notable changes to EventLog will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2024-10-30

### Added - MVP Release

#### Core System
- EventLogCollector custom component for monitoring HA Core logs
- Event categorization system (critical, major, minor, warning, log)
- Event lifecycle management (active → acknowledged → closed → archived)
- Deduplication system with configurable time windows
- Home Assistant helpers for event storage (input_text, input_select, input_boolean, input_number)

#### Components
- `event_log_collector` - Custom component for HA Core log monitoring
- `event_logger` - Main blueprint automation for event processing
- `log_event` - Script for manually creating events
- `acknowledge_event` - Script for acknowledging events
- `close_event` - Script for closing resolved events

#### Configuration
- Input text helpers for event storage
- Input select helpers for category/status/level selection
- Input boolean helpers for feature toggles
- Input number helpers for configuration values

#### Dashboard
- Lovelace event log card for Valiug dashboard
- Event display with categorization and filtering
- Configuration interface for EventLog settings

#### Documentation
- README.md - Project overview
- ARCHITECTURE.md - System design and data flow
- CONFIGURATION_GUIDE.md - Installation and setup instructions
- QUICK_START.md - Get started in 10 minutes
- CHANGELOG.md - This file

#### Examples
- sample_events.yaml - Example event entries for different categories

### Features
- Monitor home-assistant.log for errors, warnings, and critical events
- Automatically extract and categorize log entries
- Prevent duplicate events with configurable dedup window
- Store events in Home Assistant helpers
- User can acknowledge events (mark as seen)
- User can close events (mark as resolved)
- Auto-archive closed events after configurable period
- Display in Valiug dashboard with filtering/sorting

### Limitations (MVP)
- Single event source (HA Core logs only)
- Helper storage limited by input_text character limit (~2048 chars)
- No InfluxDB integration yet
- No event notification system
- Dashboard card is basic (requires custom templates)
- No event statistics/reporting yet

### Known Issues
- JSON size constraints in input_text helpers - may need pagination for large event counts
- No built-in pagination for event list display
- Dashboard card requires manual refresh in some cases

### Future Roadmap

#### Phase 2 (Event Source Integration)
- Plant Monitor integration events
- Battery status from ZHA/Zigbee2MQTT
- Device connectivity monitoring
- Climate/temperature alerts
- Network monitoring events

#### Phase 3 (Advanced Features)
- InfluxDB integration for analytics
- Event notification system (email, Slack, push)
- Event statistics and reporting dashboard
- Event export/import functionality
- Event search and advanced filtering
- Custom event blueprints

#### Phase 4 (UI/UX Improvements)
- Custom Lovelace card development
- Advanced filtering interface
- Event timeline visualization
- Statistics dashboard
- Mobile-friendly display

#### Phase 5 (Automation & Intelligence)
- Event escalation rules
- Automatic action triggers
- Machine learning for anomaly detection
- Event correlation analysis
- Predictive alerts

## Installation Notes

### Breaking Changes
None - this is initial MVP release.

### Migration Guide
N/A - new project.

### Upgrade Path
No upgrade needed for 0.1.0 (fresh installation).

## Contributors
- Alvin366 - Project creator and primary developer

## License
MIT License - See LICENSE file for details

---

## Version History

### Future Versions Expected
- 0.2.0 - InfluxDB integration
- 0.3.0 - Event sources (plant, battery, climate)
- 0.4.0 - Notification system
- 0.5.0 - Advanced UI and custom card
- 1.0.0 - Production ready release

---

## Getting Help

- GitHub Issues: https://github.com/Alvin366/EventLog/issues
- Discussions: https://github.com/Alvin366/EventLog/discussions
- Documentation: See docs/ directory

## Reporting Bugs

Found a bug? Please report it:
1. Check existing issues first
2. Provide Home Assistant version and EventLog version
3. Include steps to reproduce
4. Attach relevant logs from home-assistant.log

## Feature Requests

Have an idea? Create a GitHub discussion or issue with:
1. Clear description of feature
2. Why it would be useful
3. Any implementation ideas or examples

---

**Last Updated**: 2024-10-30
**Maintained by**: Alvin366

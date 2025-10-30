# EventLog Scripts

Scripts for EventLog system integration with Home Assistant.

## Scripts

### log_event.yaml
Manually create and log a new event to the event log.

**Parameters**:
- `category` (required): Event severity level (critical, major, minor, warning, log)
- `source` (required): Event source identifier
- `title` (required): Short event title
- `message` (required): Detailed event description
- `recommended_action` (optional): Suggested action to resolve
- `deduplication_key` (optional): Custom dedup key

**Example**:
```yaml
service: script.log_event
data:
  category: "major"
  source: "custom_integration"
  title: "Device Connection Lost"
  message: "Kitchen sensor has been offline for 30 minutes"
  recommended_action: "Check device power and WiFi connection"
  deduplication_key: "device_kitchen_sensor_offline"
```

### acknowledge_event.yaml
Acknowledge an active event (mark as seen).

**Parameters**:
- `event_id` (required): ID of event to acknowledge
- `note` (optional): Acknowledgment note

**Example**:
```yaml
service: script.acknowledge_event
data:
  event_id: "evt_20241030_140000_abc123"
  note: "Investigating this issue now"
```

### close_event.yaml
Close a resolved event (mark as resolved).

**Parameters**:
- `event_id` (required): ID of event to close
- `resolution_note` (optional): How was it resolved

**Example**:
```yaml
service: script.close_event
data:
  event_id: "evt_20241030_140000_abc123"
  resolution_note: "Device rebooted successfully"
```

## Usage in Automations

### Example: Create Event from Automation
```yaml
automation:
  - alias: "Device Offline Detection"
    trigger:
      platform: state
      entity_id: sensor.kitchen_sensor
      to: unavailable
      for:
        minutes: 5
    action:
      - service: script.log_event
        data:
          category: "minor"
          source: "device_monitor"
          title: "Device Offline"
          message: "Kitchen sensor has been unavailable for 5 minutes"
          recommended_action: "Check device power and connectivity"
          deduplication_key: "device_offline_kitchen_sensor"
```

### Example: Auto-Acknowledge
```yaml
automation:
  - alias: "Auto-Acknowledge Network Events"
    trigger:
      platform: state
      entity_id: input_text.eventlog_active_events
    action:
      - service: script.acknowledge_event
        data:
          event_id: "{{ trigger.to_state.state }}"
          note: "Automatically acknowledged by network recovery"
```

### Example: Auto-Close on Condition
```yaml
automation:
  - alias: "Auto-Close Battery Event When Charged"
    trigger:
      platform: numeric_state
      entity_id: sensor.device_battery
      above: 50
    action:
      - service: script.close_event
        data:
          event_id: "{{ state_attr('input_text.eventlog_active_events', 'battery_low_event_id') }}"
          resolution_note: "Device battery recharged above 50%"
```

## Script Development

### Adding New Scripts

1. Create new YAML file in this directory
2. Name format: `<action>_<object>.yaml`
3. Follow existing script structure
4. Add documentation
5. Update this README
6. Test in Home Assistant

### Best Practices

- Use clear parameter names
- Include default values where appropriate
- Add meaningful descriptions
- Keep scripts focused on single action
- Handle errors gracefully
- Log important actions

## Integration Points

Scripts can be called from:
- Automations (service call)
- Developer Tools (Services)
- Other scripts
- Templates
- Frontend (via UI buttons)

## Error Handling

All scripts include:
- State existence checks
- JSON parsing error handling
- Graceful fallbacks
- System log entries for debugging

## Performance Notes

- Scripts run synchronously
- Event storage is rapid
- No blocking operations
- Safe for frequent calls
- Scales to hundreds of events

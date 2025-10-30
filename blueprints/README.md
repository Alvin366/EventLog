# EventLog Blueprints

Home Assistant automation blueprints for EventLog system.

## Available Blueprints

### event_logger.yaml
Main event logger blueprint - processes events from EventLogCollector.

**Purpose**:
- Receives events from the log collector
- Handles deduplication
- Stores events in helpers
- Manages event lifecycle

**Setup**:
1. Go to Settings → Blueprints → Import Blueprint
2. Paste: `https://github.com/Alvin366/EventLog/blob/main/blueprints/event_logger.yaml`
3. Click Import
4. Create automation from blueprint
5. Configure options

**Configuration Options**:
- Collect HA Core Log Events (toggle)
- Minimum Event Category (critical, major, minor, warning, log)
- Enable Acknowledgment (toggle)
- Enable Closure (toggle)
- Enable Auto Archive (toggle)

**How It Works**:
```
EventLogCollector detects log entry
         ↓
Fires event: event_log_collector.event_detected
         ↓
Blueprint automation triggers
         ↓
Validates event data
         ↓
Checks for duplicates
         ↓
Updates existing or creates new event
         ↓
Stores in input_text.eventlog_active_events
```

## Creating Custom Blueprints

To create a new event source blueprint:

1. **Basic Structure**
```yaml
blueprint:
  name: "MyEvent Source"
  description: "Description of what this blueprint does"
  domain: automation
  source_url: "https://github.com/Alvin366/EventLog/..."

  input:
    # Your input parameters here
    entity_to_monitor:
      name: "Entity to Monitor"
      selector:
        entity:

trigger:
  # Your trigger condition here
  platform: state
  entity_id: !input entity_to_monitor

action:
  # Call log_event script
  - service: script.log_event
    data:
      category: "minor"
      source: "my_source"
      title: "My Event Title"
      message: "Event message"
      recommended_action: "What to do"
      deduplication_key: "unique_key_here"
```

2. **Example: Battery Low Event Source**
```yaml
blueprint:
  name: "Battery Low Event Source"
  description: "Creates event when battery level is low"
  domain: automation
  input:
    battery_sensor:
      name: "Battery Sensor"
      selector:
        entity:
          domain: sensor
          device_class: battery

    threshold:
      name: "Battery Threshold (%)"
      default: 20
      selector:
        number:
          min: 5
          max: 50

trigger:
  platform: numeric_state
  entity_id: !input battery_sensor
  below: !input threshold

action:
  - service: script.log_event
    data:
      category: "minor"
      source: "battery_monitor"
      title: "Low Battery: {{ state_attr(trigger.entity_id, 'friendly_name') }}"
      message: "Battery level is {{ states(trigger.entity_id) }}%"
      recommended_action: "Replace or charge battery"
      deduplication_key: "battery_low_{{ trigger.entity_id }}"
```

3. **Example: Plant Watering Event Source**
```yaml
blueprint:
  name: "Plant Watering Event Source"
  description: "Creates event when plant needs watering"
  domain: automation
  input:
    soil_moisture:
      name: "Soil Moisture Sensor"
      selector:
        entity:
          domain: sensor

    threshold:
      name: "Moisture Threshold (%)"
      default: 30
      selector:
        number:
          min: 10
          max: 50

trigger:
  platform: numeric_state
  entity_id: !input soil_moisture
  below: !input threshold

action:
  - service: script.log_event
    data:
      category: "minor"
      source: "plant_monitor"
      title: "Plant Watering: {{ state_attr(trigger.entity_id, 'friendly_name') }}"
      message: "Soil moisture is {{ states(trigger.entity_id) }}%"
      recommended_action: "Water the plant"
      deduplication_key: "plant_water_{{ trigger.entity_id }}"
```

## Best Practices for Blueprint Development

1. **Naming**
   - Use descriptive names
   - Include event type in name
   - Use lowercase with hyphens for file names

2. **Documentation**
   - Clear blueprint description
   - Explain what each input does
   - Provide examples in YAML

3. **Triggers**
   - Use platform-specific triggers
   - Avoid excessive polling
   - Combine conditions efficiently

4. **Actions**
   - Always call script.log_event
   - Use consistent categorization
   - Provide useful messages
   - Include recommended actions

5. **Deduplication Keys**
   - Make unique but consistent
   - Include entity ID or device name
   - Use format: `source_type_identifier`
   - Example: `battery_low_kitchen_sensor`

6. **Categories**
   - Use appropriate severity levels
   - Consider user impact
   - Match with notification importance

7. **Testing**
   - Test with actual data
   - Verify deduplication works
   - Check message clarity
   - Monitor event creation

## Submitting Blueprints

To share your blueprint:

1. Create well-documented YAML file
2. Test thoroughly in your Home Assistant
3. Create GitHub issue with blueprint content
4. Include examples and use cases
5. Describe what events it creates

Accepted blueprints will be added to repository!

## Blueprint Resources

- Home Assistant Blueprint Docs: https://www.home-assistant.io/docs/blueprint/
- Blueprint Community: https://community.home-assistant.io/c/blueprints/
- EventLog GitHub: https://github.com/Alvin366/EventLog

## Troubleshooting Blueprints

### Blueprint Won't Import
- Check syntax (YAML format)
- Verify indentation
- Check GitHub URL is correct

### Automation Not Triggering
- Check trigger conditions
- Verify entity IDs exist
- Check automation is enabled
- Review Home Assistant logs

### Events Not Being Created
- Verify script.log_event exists
- Check service calls in logs
- Verify required parameters
- Test script manually

## Contributing

Found an issue or have a better blueprint?
1. Report issue on GitHub
2. Include blueprint YAML
3. Describe the problem
4. Share test data if possible

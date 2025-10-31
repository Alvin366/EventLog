# EventLog - Developer Guide

## Project Structure

```
EventLog/
├── .github/workflows/          # CI/CD pipelines
├── blueprints/                 # Home Assistant blueprints
│   └── event_logger.yaml      # Main event logger blueprint
├── custom_components/          # Custom integrations
│   └── event_log_collector/   # Log monitoring component
├── automations/                # Automation files
├── scripts/                    # Script definitions
├── config/                     # Helper configurations
├── docs/                       # Documentation
├── lovelace/                   # Dashboard cards
├── examples/                   # Example files
├── tests/                      # Test files
├── CHANGELOG.md               # Version history
├── QUICK_START.md             # Quick start guide
└── README.md                  # Main documentation
```

## Development Setup

### Prerequisites
- Home Assistant 2024.9.0+
- Python 3.11+
- Git

### Local Testing

1. Clone the repository
2. Copy files to Home Assistant config directory
3. Test components locally before deployment

## Component Development: EventLogCollector

### Location
`custom_components/event_log_collector/__init__.py`

### Key Classes

**LogFileCollector**
- Monitors Home Assistant log file
- Parses log lines to extract events
- Categorizes by log level
- Fires events for automation processing

### Methods

```python
async def _monitor_loop()
  - Continuous monitoring loop
  - Scans log file at configured interval
  - Handles log rotation

async def _check_log_file()
  - Reads new lines from log file
  - Updates position tracking
  - Processes each line

async def _process_log_line(line: str)
  - Parses individual log line
  - Checks against ignore keywords
  - Extracts event information
  - Fires event_log_collector.event_detected

def _parse_log_line(line: str) -> Dict
  - Extracts timestamp, log level, context
  - Determines event category
  - Generates deduplication key
  - Returns structured event data
```

## Blueprint Development: event_logger.yaml

### Flow
1. Trigger: Receives `event_log_collector.event_detected`
2. Condition: Validates event and checks minimum level
3. Action: Processes event through deduplication
4. Action: Stores to helpers or InfluxDB

### Key Variables
- `category` - Event severity level
- `dedup_key` - Unique identifier for deduplication
- `timestamp` - When event occurred
- `is_duplicate` - Whether event already exists

## Script Development

### Available Scripts

**log_event.yaml**
- Adds new event to event log
- Accepts custom parameters
- Creates event entry with metadata

**acknowledge_event.yaml**
- Moves event from active to acknowledged
- Preserves event data
- Marks with acknowledgment time and note

**close_event.yaml**
- Moves event from active to closed
- Moves to archive
- Removes from active list

## Testing Guidelines

### Unit Testing
- Test log line parsing
- Test event categorization
- Test deduplication logic

### Integration Testing
- Test with actual Home Assistant
- Monitor real log file
- Verify event storage
- Test dashboard display

### Edge Cases
- Log file rotation
- Large log file handling
- Empty/malformed log lines
- Concurrent event processing

## Contribution Process

1. Create feature branch from `main`
2. Make changes with clear commits
3. Test thoroughly on Home Assistant instance
4. Update documentation
5. Create pull request with description
6. Address review feedback
7. Merge when approved

## Code Style

### Python
- Follow PEP 8
- Use type hints
- Add docstrings
- Keep lines under 100 chars

### YAML
- Use 2-space indentation
- Consistent key naming
- Include descriptions
- Keep files organized

### Git Commits
- Clear, concise messages
- Reference issues when applicable
- Format: `type: brief description`
  - `feat: add new feature`
  - `fix: resolve bug`
  - `docs: update documentation`
  - `refactor: code improvement`

## Performance Considerations

### Log File Monitoring
- Efficient seeking to avoid re-reading
- Configurable scan interval
- Handle large log files gracefully

### Event Storage
- JSON serialization for helpers
- Limit event count (archive old)
- Avoid excessive state updates

### Blueprint Automation
- Use conditions to reduce processing
- Batch updates when possible
- Clean up archived events

## Debugging

### Enable Debug Logging
In `configuration.yaml`:
```yaml
logger:
  default: info
  logs:
    event_log_collector: debug
    homeassistant.automation: debug
```

### Monitor Logs
```bash
tail -f /config/home-assistant.log | grep eventlog
```

### Check States
Developer Tools → States → search for eventlog entities

### Test Service Calls
Developer Tools → Services → manually trigger events

## Documentation

### Adding Documentation
1. Create markdown file in `docs/`
2. Update `README.md` to link to it
3. Keep documentation up-to-date with code

### Documentation Structure
- Title with clear purpose
- Table of contents for longer docs
- Code examples with context
- Troubleshooting section
- Links to related docs

## Deployment & Cache Management

### Pushing Blueprint Updates to GitHub

After making changes to blueprint files:

```bash
cd /config/ClaudeProjects/EventLog
git add blueprints/eventlog_master.yaml
git commit -m "fix: Description of changes"
git push origin main
```

### IMPORTANT: Home Assistant Blueprint Caching

Home Assistant caches blueprint definitions in the browser. After pushing new blueprint code to GitHub, you **MUST** clear the cache in Home Assistant before re-importing:

**Step 1: Delete the Old Blueprint**
- Settings → Automations & Scenes → Blueprints
- Find the blueprint you modified
- Click the three dots (⋯) menu
- Click "Delete blueprint"
- Confirm deletion

**Step 2: Hard Refresh Browser Cache**
- Press **Ctrl+Shift+Delete** (Windows) or **Cmd+Shift+Delete** (Mac)
- OR press **Ctrl+Shift+R** / **Cmd+Shift+R** on the blueprints page

**Step 3: Re-import with Raw GitHub URL**
- Use the raw GitHub URL to bypass URL caching:
  ```
  https://raw.githubusercontent.com/Alvin366/EventLog/main/blueprints/eventlog_master.yaml
  ```
- NOT the regular GitHub web URL
- Home Assistant will fetch the latest version

**Why This Is Necessary:**
- GitHub serves blueprint files from the web, which get cached by browsers
- Home Assistant also caches blueprint definitions in memory
- The raw URL forces fetching the true latest content
- This is a known limitation of blueprint imports

### Troubleshooting Cache Issues

If you still see old blueprint errors after clearing cache:

1. **Check Git Logs to Confirm Push**
   ```bash
   git log --oneline -3
   ```
   Verify your latest commit is listed

2. **Wait 1-2 Minutes**
   GitHub CDN may take time to serve the latest version

3. **Check GitHub Directly**
   Visit: https://raw.githubusercontent.com/Alvin366/EventLog/main/blueprints/eventlog_master.yaml
   Verify the latest code is there

4. **Clear All HA Caches**
   - Hard refresh browser (Ctrl+Shift+Delete)
   - Clear browser cookies for home-assistant instance
   - Restart Home Assistant (Settings → System → Restart Home Assistant)

## Version Management

### Semantic Versioning
- `MAJOR.MINOR.PATCH-PRERELEASE`
- Example: `0.1.0-MVP`

### Release Process
1. Update VERSION file
2. Update CHANGELOG.md
3. Commit with version tag
4. Push to main branch
5. Create GitHub release
6. Users must clear cache and re-import blueprint

## Future Development

### Planned Features
- Additional event sources (plant monitor, battery, climate)
- InfluxDB integration for analytics
- Event notification system
- Advanced dashboard UI
- Event correlation and escalation
- Custom event templates

### Architecture Improvements
- Event persistence layer
- Better deduplication strategy
- Event compression for storage
- Distributed event collection
- Event streaming support

## Getting Help

### Resources
- Home Assistant Developer Docs: https://developers.home-assistant.io/
- Blueprint Documentation: https://www.home-assistant.io/docs/blueprint/
- Python HA Components: https://github.com/home-assistant/home-assistant

### Community
- GitHub Issues: https://github.com/Alvin366/EventLog/issues
- Discussions: https://github.com/Alvin366/EventLog/discussions
- Home Assistant Forums: https://community.home-assistant.io/

## License

This project is licensed under MIT License - see LICENSE file for details.

All contributions must agree to this license.

---

**Last Updated**: 2024-10-30
**Maintained by**: Alvin366

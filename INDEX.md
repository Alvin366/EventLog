# EventLog Project Index

**Navigation guide for all EventLog documentation and code**

---

## Getting Started (Read These First)

1. **[README.md](README.md)** - Start here! Project overview and features
2. **[QUICK_START.md](QUICK_START.md)** - Get running in 10 minutes
3. **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - What's been completed and what's next
4. **[DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)** - Step-by-step deployment guide

---

## Documentation

### Core Documentation
- **[ARCHITECTURE.md](docs/ARCHITECTURE.md)** - System design, components, data flows
- **[CONFIGURATION_GUIDE.md](docs/CONFIGURATION_GUIDE.md)** - Detailed installation instructions
- **[CHANGELOG.md](CHANGELOG.md)** - Version history and release notes

### Developer Documentation
- **[README_DEVELOPERS.md](README_DEVELOPERS.md)** - For developers and contributors
- **[docs/README.md](docs/README.md)** - Documentation index and reference

### Component Documentation
- **[blueprints/README.md](blueprints/README.md)** - Blueprint development guide
- **[scripts/README.md](scripts/README.md)** - Script documentation
- **[config/README.md](config/README.md)** - Helper configuration reference

---

## Source Code

### Custom Components
```
custom_components/
└── event_log_collector/        Main component for log monitoring
    ├── __init__.py             Core logic (LogFileCollector class)
    └── manifest.json           Component metadata
```

### Blueprints
```
blueprints/
├── event_logger.yaml           Main event logger blueprint
└── README.md                   Blueprint development guide
```

### Scripts
```
scripts/
├── log_event.yaml              Create new event
├── acknowledge_event.yaml      Acknowledge event
├── close_event.yaml            Close event
└── README.md                   Script documentation
```

### Configuration
```
config/
├── input_text.yaml             JSON storage helpers
├── input_select.yaml           Dropdown selectors
├── input_boolean.yaml          Feature toggles
├── input_number.yaml           Numeric configuration
└── README.md                   Configuration reference
```

### Dashboard
```
lovelace/
└── event_log_card.yaml         Valiug dashboard card
```

### Examples
```
examples/
└── sample_events.yaml          Example event entries
```

---

## Project Files

### Metadata
- **[VERSION](VERSION)** - Current version (0.1.0-MVP)
- **[LICENSE](LICENSE)** - MIT License
- **[.gitignore](.gitignore)** - Git ignore patterns

### Documentation
- **[README.md](README.md)** - Main project documentation
- **[QUICK_START.md](QUICK_START.md)** - Quick setup guide
- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Completion summary
- **[DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)** - Deployment steps
- **[CHANGELOG.md](CHANGELOG.md)** - Version history
- **[INDEX.md](INDEX.md)** - This file
- **[README_DEVELOPERS.md](README_DEVELOPERS.md)** - Developer guide

### Directories
- **[docs/](docs/)** - Detailed documentation
- **[blueprints/](blueprints/)** - Automation blueprints
- **[custom_components/](custom_components/)** - Custom integrations
- **[scripts/](scripts/)** - Home Assistant scripts
- **[config/](config/)** - Helper configurations
- **[lovelace/](lovelace/)** - Dashboard cards
- **[examples/](examples/)** - Example data
- **[tests/](tests/)** - Testing directory (ready for tests)
- **[automations/](automations/)** - Additional automations (ready for future use)
- **[.github/](.github/)** - GitHub configuration (ready for workflows)

---

## Quick Reference

### Key Concepts

**Event Categories**:
- `critical` - System failures, security events
- `major` - Component issues, device offline
- `minor` - Low battery, watering needed
- `warning` - Threshold alerts, non-critical issues
- `log` - Informational messages

**Event Lifecycle**:
```
active → acknowledged → closed → archived
   ↓                               ↑
   └─── auto-resolve (timeout) ───┘
```

**Key Entities**:
- `input_text.eventlog_active_events` - Currently active events
- `input_text.eventlog_acknowledged_events` - Acknowledged events
- `input_text.eventlog_archive` - Archived/closed events
- `input_boolean.eventlog_enabled` - Master enable/disable
- `input_number.eventlog_archive_days` - Archive period in days

### Services

**Create Event**:
```yaml
service: script.log_event
data:
  category: "minor"
  source: "custom"
  title: "Event title"
  message: "Event details"
  recommended_action: "What to do"
  deduplication_key: "unique_key"
```

**Acknowledge Event**:
```yaml
service: script.acknowledge_event
data:
  event_id: "evt_xxxx"
  note: "Acknowledgment note"
```

**Close Event**:
```yaml
service: script.close_event
data:
  event_id: "evt_xxxx"
  resolution_note: "How it was resolved"
```

---

## Development Workflow

### For Deployment
1. Read: **[QUICK_START.md](QUICK_START.md)**
2. Review: **[CONFIGURATION_GUIDE.md](docs/CONFIGURATION_GUIDE.md)**
3. Follow: **[DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)**
4. Test: Verify all checks pass

### For Understanding
1. Read: **[README.md](README.md)** - Overview
2. Read: **[ARCHITECTURE.md](docs/ARCHITECTURE.md)** - How it works
3. Browse: Code files in respective directories
4. Check: **[README_DEVELOPERS.md](README_DEVELOPERS.md)** for technical details

### For Contributing
1. Review: **[README_DEVELOPERS.md](README_DEVELOPERS.md)**
2. Check: **[blueprints/README.md](blueprints/README.md)** for blueprint development
3. Check: **[scripts/README.md](scripts/README.md)** for script development
4. Test: Thoroughly before submitting

### For Troubleshooting
1. Check: **[CONFIGURATION_GUIDE.md](docs/CONFIGURATION_GUIDE.md)** Troubleshooting section
2. Review: **[home-assistant.log](home-assistant.log)** for errors
3. Check: **[DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)** verification steps
4. Create: GitHub issue with details

---

## File Organization

### By Purpose

**Installation & Setup**:
- [QUICK_START.md](QUICK_START.md)
- [CONFIGURATION_GUIDE.md](docs/CONFIGURATION_GUIDE.md)
- [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)

**Understanding System**:
- [ARCHITECTURE.md](docs/ARCHITECTURE.md)
- [README_DEVELOPERS.md](README_DEVELOPERS.md)

**Extending System**:
- [blueprints/README.md](blueprints/README.md)
- [scripts/README.md](scripts/README.md)
- [config/README.md](config/README.md)

**Reference**:
- [README.md](README.md)
- [CHANGELOG.md](CHANGELOG.md)
- [examples/sample_events.yaml](examples/sample_events.yaml)

---

## Directory Tree

```
EventLog/
├── blueprints/
│   ├── event_logger.yaml
│   └── README.md
├── custom_components/
│   └── event_log_collector/
│       ├── __init__.py
│       └── manifest.json
├── scripts/
│   ├── log_event.yaml
│   ├── acknowledge_event.yaml
│   ├── close_event.yaml
│   └── README.md
├── config/
│   ├── input_text.yaml
│   ├── input_select.yaml
│   ├── input_boolean.yaml
│   ├── input_number.yaml
│   └── README.md
├── lovelace/
│   └── event_log_card.yaml
├── docs/
│   ├── ARCHITECTURE.md
│   ├── CONFIGURATION_GUIDE.md
│   ├── EVENT_SOURCES.md
│   ├── DEVELOPMENT.md
│   └── README.md
├── examples/
│   └── sample_events.yaml
├── tests/
│   └── (ready for test files)
├── automations/
│   └── (ready for additional automations)
├── .github/
│   └── workflows/
│       └── (ready for CI/CD workflows)
├── README.md
├── QUICK_START.md
├── PROJECT_SUMMARY.md
├── DEPLOYMENT_CHECKLIST.md
├── CHANGELOG.md
├── README_DEVELOPERS.md
├── INDEX.md (this file)
├── VERSION
├── LICENSE
└── .gitignore
```

---

## What's Next?

### Immediate (This Week)
1. Review [README.md](README.md) and [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)
2. Decide on deployment approach
3. Follow [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)
4. Deploy and test MVP

### Short Term (This Month)
1. Run system for 7 days
2. Monitor stability and collect feedback
3. Plan Phase 2 event sources
4. Document any issues found

### Medium Term (This Quarter)
1. Implement Phase 2 (additional event sources)
2. Add Phase 3 (InfluxDB integration)
3. Begin advanced features
4. Approach v1.0 production release

---

## Support & Resources

### Getting Help
- **Installation Issues**: See [CONFIGURATION_GUIDE.md](docs/CONFIGURATION_GUIDE.md) troubleshooting
- **Architecture Questions**: See [ARCHITECTURE.md](docs/ARCHITECTURE.md)
- **Development Help**: See [README_DEVELOPERS.md](README_DEVELOPERS.md)
- **GitHub Issues**: https://github.com/Alvin366/EventLog/issues

### Key Commands
```bash
# Copy component
cp -r custom_components/event_log_collector /config/custom_components/

# Check logs
tail -f /config/home-assistant.log | grep eventlog

# Validate YAML
python3 -m yaml -c config/input_text.yaml
```

### Links
- **GitHub**: https://github.com/Alvin366/EventLog
- **Home Assistant**: https://www.home-assistant.io/
- **Valiug Dashboard**: [Your Valiug repo]
- **HA Blueprints**: https://www.home-assistant.io/blueprints/

---

## Document Status

| Document | Status | Last Updated |
|----------|--------|--------------|
| README.md | ✅ Complete | 2024-10-30 |
| QUICK_START.md | ✅ Complete | 2024-10-30 |
| ARCHITECTURE.md | ✅ Complete | 2024-10-30 |
| CONFIGURATION_GUIDE.md | ✅ Complete | 2024-10-30 |
| DEPLOYMENT_CHECKLIST.md | ✅ Complete | 2024-10-30 |
| PROJECT_SUMMARY.md | ✅ Complete | 2024-10-30 |
| README_DEVELOPERS.md | ✅ Complete | 2024-10-30 |
| blueprints/README.md | ✅ Complete | 2024-10-30 |
| scripts/README.md | ✅ Complete | 2024-10-30 |
| config/README.md | ✅ Complete | 2024-10-30 |
| CHANGELOG.md | ✅ Complete | 2024-10-30 |
| INDEX.md | ✅ Complete | 2024-10-30 |

---

## Quick Links by Task

### "I want to install EventLog"
→ [QUICK_START.md](QUICK_START.md) → [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)

### "I want to understand how it works"
→ [README.md](README.md) → [ARCHITECTURE.md](docs/ARCHITECTURE.md) → [docs/README.md](docs/README.md)

### "I want to extend/modify it"
→ [README_DEVELOPERS.md](README_DEVELOPERS.md) → [blueprints/README.md](blueprints/README.md) → Source code

### "I found an issue"
→ [CONFIGURATION_GUIDE.md](docs/CONFIGURATION_GUIDE.md#troubleshooting) → [home-assistant.log] → GitHub issue

### "I want to add event sources"
→ [blueprints/README.md](blueprints/README.md) → Create custom blueprint → Test

### "I want to see the code"
→ [custom_components/](custom_components/) → [blueprints/](blueprints/) → [scripts/](scripts/)

---

**Navigation Index Version**: 0.1.0-MVP
**Last Updated**: 2024-10-30
**Maintained by**: Alvin366

---

## Feedback

Found something unclear in this index? Create a GitHub issue with:
- What you were trying to do
- What document you need help with
- What could be clearer

Your feedback helps improve EventLog! 🙏

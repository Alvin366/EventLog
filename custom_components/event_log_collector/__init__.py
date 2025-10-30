"""EventLogCollector - Home Assistant Core Log Event Collector."""

import asyncio
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

import voluptuous as vol
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_ENABLED, CONF_NAME
from homeassistant.core import HomeAssistant, callback
from homeassistant.exceptions import ConfigValidationError
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.typing import ConfigType

_LOGGER = logging.getLogger(__name__)

DOMAIN = "event_log_collector"
EVENT_DETECTED = "event_log_collector.event_detected"

CONF_LOG_FILE = "log_file"
CONF_SCAN_INTERVAL = "scan_interval"
CONF_MAX_LOG_SIZE = "max_log_size"
CONF_CATEGORIES = "categories"
CONF_IGNORE_KEYWORDS = "ignore_keywords"
CONF_CRITICAL_KEYWORDS = "critical_keywords"

DEFAULT_LOG_FILE = "/config/home-assistant.log"
DEFAULT_SCAN_INTERVAL = 60
DEFAULT_MAX_LOG_SIZE = 10485760  # 10MB

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.All(
            cv.ensure_list,
            [
                vol.Schema(
                    {
                        vol.Required(CONF_ENABLED, default=True): cv.boolean,
                        vol.Optional(CONF_LOG_FILE, default=DEFAULT_LOG_FILE): cv.string,
                        vol.Optional(
                            CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL
                        ): cv.positive_int,
                        vol.Optional(
                            CONF_MAX_LOG_SIZE, default=DEFAULT_MAX_LOG_SIZE
                        ): cv.positive_int,
                        vol.Optional(
                            CONF_CATEGORIES,
                            default={"ERROR": "major", "WARNING": "warning", "CRITICAL": "critical"},
                        ): {cv.string: cv.string},
                        vol.Optional(CONF_IGNORE_KEYWORDS, default=[]): cv.ensure_list,
                        vol.Optional(CONF_CRITICAL_KEYWORDS, default=[]): cv.ensure_list,
                    },
                    extra=vol.ALLOW_EXTRA,
                )
            ],
        ),
    },
    extra=vol.ALLOW_EXTRA,
)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up EventLogCollector."""
    hass.data[DOMAIN] = {}

    if DOMAIN not in config:
        return True

    # Get first config (support single instance)
    collector_config = config[DOMAIN][0]

    if not collector_config.get(CONF_ENABLED):
        _LOGGER.info("EventLogCollector is disabled")
        return True

    try:
        log_collector = LogFileCollector(hass, collector_config)
        hass.data[DOMAIN]["collector"] = log_collector

        # Start monitoring
        hass.async_create_task(log_collector.async_start())

        _LOGGER.info(
            "EventLogCollector started, monitoring: %s",
            collector_config.get(CONF_LOG_FILE),
        )

    except Exception as err:
        _LOGGER.error("Error setting up EventLogCollector: %s", err)
        raise ConfigValidationError(f"Invalid EventLogCollector configuration: {err}")

    return True


class LogFileCollector:
    """Monitor Home Assistant log file and extract events."""

    def __init__(self, hass: HomeAssistant, config: Dict[str, Any]) -> None:
        """Initialize log collector."""
        self.hass = hass
        self.config = config
        self.log_file = Path(config.get(CONF_LOG_FILE, DEFAULT_LOG_FILE))
        self.scan_interval = config.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)
        self.max_log_size = config.get(CONF_MAX_LOG_SIZE, DEFAULT_MAX_LOG_SIZE)
        self.categories = config.get(
            CONF_CATEGORIES,
            {"ERROR": "major", "WARNING": "warning", "CRITICAL": "critical"},
        )
        self.ignore_keywords = config.get(CONF_IGNORE_KEYWORDS, [])
        self.critical_keywords = config.get(CONF_CRITICAL_KEYWORDS, [])
        self.last_position = 0
        self.last_size = 0
        self._cancel_task = None

    async def async_start(self) -> None:
        """Start monitoring log file."""
        # Initial position
        if self.log_file.exists():
            self.last_size = self.log_file.stat().st_size

        # Start monitoring loop
        self._cancel_task = self.hass.async_create_task(self._monitor_loop())

    async def _monitor_loop(self) -> None:
        """Monitor log file for new events."""
        while True:
            try:
                await asyncio.sleep(self.scan_interval)

                if not self.log_file.exists():
                    _LOGGER.warning("Log file not found: %s", self.log_file)
                    continue

                await self._check_log_file()

            except asyncio.CancelledError:
                break
            except Exception as err:
                _LOGGER.error("Error monitoring log file: %s", err)

    async def _check_log_file(self) -> None:
        """Check log file for new events."""
        try:
            current_size = self.log_file.stat().st_size

            # Handle log rotation
            if current_size < self.last_size:
                _LOGGER.debug("Log file rotated, resetting position")
                self.last_position = 0

            if current_size <= self.last_position:
                return

            # Read new data
            with open(self.log_file, "r", encoding="utf-8") as f:
                f.seek(self.last_position)
                new_lines = f.readlines()
                self.last_position = f.tell()

            self.last_size = current_size

            # Process new lines
            for line in new_lines:
                await self._process_log_line(line.strip())

        except Exception as err:
            _LOGGER.error("Error reading log file: %s", err)

    async def _process_log_line(self, line: str) -> None:
        """Process a single log line and extract events."""
        if not line:
            return

        # Check ignore keywords
        for keyword in self.ignore_keywords:
            if keyword.lower() in line.lower():
                return

        # Extract log level and message
        event_data = self._parse_log_line(line)
        if event_data:
            # Fire event for automation to catch
            self.hass.bus.async_fire(EVENT_DETECTED, event_data)

    def _parse_log_line(self, line: str) -> Dict[str, Any] | None:
        """Parse log line and extract event information."""
        try:
            # Expected format: YYYY-MM-DD HH:MM:SS LEVEL (Context) [Module] Message
            # Example: 2024-10-30 14:00:00 ERROR (MainThread) [homeassistant.auth] Failed login

            parts = line.split()
            if len(parts) < 3:
                return None

            # Extract timestamp
            try:
                timestamp = f"{parts[0]} {parts[1]}"
                datetime.fromisoformat(timestamp)
            except ValueError:
                return None

            # Extract log level
            log_level = None
            level_index = -1

            for i, part in enumerate(parts[2:], start=2):
                if part in self.categories:
                    log_level = part
                    level_index = i
                    break

            if not log_level:
                return None

            # Determine category
            category = self.categories.get(log_level, "log")

            # Check for critical keywords
            for keyword in self.critical_keywords:
                if keyword.lower() in line.lower():
                    category = "critical"
                    break

            # Extract context and module
            context = ""
            module = ""

            # Look for (Context) and [Module] patterns
            import re

            context_match = re.search(r"\(([^)]+)\)", line)
            if context_match:
                context = context_match.group(1)

            module_match = re.search(r"\[([^\]]+)\]", line)
            if module_match:
                module = module_match.group(1)

            # Extract message (everything after module)
            message = line[level_index + len(log_level) :].strip()
            if message.startswith("("):
                message = message.split("]", 1)[-1].strip()

            if not message:
                return None

            # Create deduplication key from module and message
            dedup_key = f"ha_core_{module.replace('.', '_')}_{message[:50].lower().replace(' ', '_')}"

            return {
                "timestamp": timestamp,
                "category": category,
                "source": "ha_core",
                "log_level": log_level,
                "context": context,
                "module": module,
                "title": f"{log_level}: {module}",
                "message": message,
                "recommended_action": self._get_recommended_action(log_level, module, message),
                "deduplication_key": dedup_key,
                "auto_resolve_timeout": self._get_auto_resolve_timeout(category),
            }

        except Exception as err:
            _LOGGER.debug("Error parsing log line '%s': %s", line, err)
            return None

    def _get_recommended_action(self, log_level: str, module: str, message: str) -> str:
        """Get recommended action based on event details."""
        if "auth" in module.lower() or "login" in message.lower():
            return "Check failed login attempt - verify credentials and network access"
        elif "integration" in module.lower():
            return "Check integration configuration and logs"
        elif "database" in module.lower():
            return "Check database connectivity and configuration"
        elif "network" in message.lower() or "connection" in message.lower():
            return "Check network connectivity and firewall settings"
        elif log_level == "CRITICAL":
            return "Review critical error and restart Home Assistant if needed"
        elif log_level == "ERROR":
            return "Review error details and check affected integration/component"
        else:
            return "Monitor situation and take action if issue persists"

    def _get_auto_resolve_timeout(self, category: str) -> int:
        """Get auto-resolve timeout based on category."""
        timeouts = {
            "critical": 3600,  # 1 hour
            "major": 7200,  # 2 hours
            "minor": 86400,  # 24 hours
            "warning": 86400,  # 24 hours
            "log": 604800,  # 7 days
        }
        return timeouts.get(category, 86400)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up from config entry (for future UI setup)."""
    return True

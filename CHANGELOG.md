# 📜 Changelog

All notable changes to this project will be documented in this file.

## [v1.0.1] - 2025-05-15

### 🐞 Fixed
- Resolved `Cannot close a running event loop` error on boot.
- Removed conflict-prone `asyncio.run()` usage.

### 🔄 Changed
- Python script now includes a boot-safe startup delay.
- Logging made more informative for troubleshooting.
- Retry mechanism is now synchronous using `time.sleep()`.

### ➕ Added
- `ExecStartPre=/bin/sleep 30` in `temp.service` to ensure delayed start.
- `network-online.target` dependency added to systemd unit.
- Retry handler in the bot script to cope with early boot failures.


## [1.0.0] - 2025-05-05
### Added
- Temperature monitoring function (`temp.py`)
- Systemd service setup guide (`temp.service`)
- Full documentation: setup, prerequisites, and bot usage
- SSH-based remote Pi access
- Virtual environment setup instructions

### Upcoming
- CPU & memory usage display
- Custom shell command execution
- Error logging and recovery features

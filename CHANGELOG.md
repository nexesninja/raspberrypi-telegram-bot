# 📜 Changelog

All notable changes to this project will be documented in this file.


## [v2.0.0] - 2025-07-07

### 🚀 Added
- Full modular structure (`main.py`, `config/`, `modules/`, `docs/`)
- Secure command execution module with input validation and rate limiting
- System monitoring: CPU, memory, and disk usage
- Automatic temperature alert system with threshold logic
- Telegram bot now uses `python-telegram-bot v20+` with `JobQueue` support
- New commands: `/system`, `/status`, `/cmd`, `/help`
- systemd service file: `pi-telegram-bot.service`
- Complete documentation: `README.md`, `installation_guide.md`, `troubleshooting.md`

### 🛡️ Security
- Authorized user ID whitelisting
- No use of `shell=True` in subprocesses
- Restricted environment paths and timeouts
- Secure logging and input sanitization

### 🔧 Changed
- Refactored single-script bot into modular structure
- Logs redirected to `logs/` folder (gitignored)
- `requirements.txt` now tracks exact versions
- Improved error handling and logging clarity

---

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

---

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

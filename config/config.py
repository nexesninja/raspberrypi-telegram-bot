# config/config.py
import os
from typing import List

# Telegram Bot Configuration
BOT_TOKEN = os.getenv('BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')

# Security: List of authorized user IDs (get from @userinfobot)
AUTHORIZED_USERS: List[int] = [
    # 123456789,  # Replace with your Telegram user ID
]

# Command whitelist for security
ALLOWED_COMMANDS = [
    'ls', 'pwd', 'whoami', 'date', 'uptime', 'df', 'free',
    'ps', 'top', 'htop', 'systemctl', 'journalctl',
    'cat', 'tail', 'head', 'grep', 'find', 'which',
    'uname', 'lscpu', 'lsusb', 'lsblk', 'mount',
    'ping', 'wget', 'curl', 'git', 'pip', 'python3'
]

# System monitoring settings
TEMP_WARNING_THRESHOLD = 70.0  # Celsius
TEMP_CRITICAL_THRESHOLD = 80.0  # Celsius
CPU_WARNING_THRESHOLD = 80.0   # Percentage
MEMORY_WARNING_THRESHOLD = 85.0  # Percentage

# Logging configuration
LOG_LEVEL = 'INFO'
LOG_FILE = 'logs/bot.log'

# Rate limiting (commands per minute per user)
RATE_LIMIT = 10

If you're running into errors, these solutions might help you.

## Monitoring
To understand the issues in the system, you can use the following commands in the terminal.
```bash
# Service status
sudo systemctl status pi-telegram-bot

# Live logs
sudo journalctl -u pi-telegram-bot -f

# Application logs
tail -f ~/pi_telegram_bot/logs/bot.log
```

## Troubleshooting
### Common Issues

<b>1. Bot Token Error</b>

- Verify token in config.py
- Check for extra spaces or characters

<b>2. Permission Denied</b>

- Check file permissions
- Ensure virtual environment is activated


<b>3. Module Import Errors</b>

- Verify directory structure
- Check __init__.py files exist


<b>4. Temperature Reading Issues</b>

- Some sensors may need additional permissions
- Check if vcgencmd is available


<b>5. Command Execution Failures</b>

- Verify command is in whitelist
- Check command syntax



## Debug Mode
Add to config.py for more verbose logging:
```bash
pythonLOG_LEVEL = 'DEBUG'
```

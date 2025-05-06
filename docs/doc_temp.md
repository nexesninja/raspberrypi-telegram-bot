# Check Temperature
  This guide explains how to set up the temperature-checking function of your Raspberry Pi Telegram Bot. All commands are intended to be run via **SSH**. If you're using the Raspberry Pi GUI, you can follow the same steps in a terminal window.

### 1️⃣ Set up the temperature-checking Script
Create file temp.py in the bot directory.  

```bash
nano ~/telegram_bot/temp.py
```
  
and paste the given code in temp.py in it.  
  
  
Now make the file executable using,  
  ```bash
chmod +x ~/telegram_bot/temp.py  
  ```

### 2️⃣ Create a Service  
Create a systemd service file.  
  ```bash
sudo nano /etc/systemd/system/temp.service
 ``` 
Paste the contents of your temp.service file. Important:  
- Replace User=pi with your actual Raspberry Pi username.  
- Update all paths to match your username and directory structure.  
- Replace the placeholder bot_token with your actual Telegram bot token (see [Prerequisites](https://github.com/nexesninja/raspberrypi-telegram-bot/blob/main/docs/prerequisites.md)).  
  
Save the file and Exit.  

Now the service can be enabled and started.  
  
    sudo systemctl daemon-reload
    sudo systemctl enable temp.service
    sudo systemctl start temp.service 
      
⚠️ Run each command separately. 

### 3️⃣ Testing the Bot
Start your bot in Telegram by `/start`.    
Available commands:
- /temp — Get the current temperature of your Raspberry Pi.
- /help — View the list of available commands (you can customize this message in your script).

If the bot isn't responding, this command will help identify issues.   
```bash
sudo systemctl status rpi-temp-bot.service
```


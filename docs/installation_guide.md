This guide explains how to set up the bot-functions of your Raspberry Pi Telegram Bot. All commands are intended to be run via SSH. If you're using the Raspberry Pi GUI, you can follow the same steps in a terminal window.<br/>

Also you can download and place the files from this repository to rpi directly.

## Create project directory

```bash
mkdir ~/pi_telegram_bot
cd ~/pi_telegram_bot
```

##Install Requirements
Download or create file `requirements.txt` and copy the details in `requirements.txt` in repo to file.  
Then run the following command.  
```bash
pip install -r requirements.txt
```
  
## Create main.py, modules and config

Place `main.py` , `modules` folder with `temperature_monitor.py, system_monitor.py, command_executor.py` and the `config` folder with `config.py` inside `pi_telegram_bot`.  
  
## Configuration

Edit `config/config.py` and replace with your actual bot token and telegram user ID. (You can add multiple IDs)

```bash
BOT_TOKEN = 'bot-token-here'

AUTHORIZED_USERS = [
    123456789,# Your user ID
]

```

## Create Empty init.py Files

```bash
touch modules/__init__.py
touch config/__init__.py

```

## Create bot.log

```bash
mkdir logs
touch logs/bot.log
```
To provide writing permissions, use following command.
```bash
chmod 644 logs/bot.log
```
  
## Test Installation

```bash
#Activate virtual environment
source venv/bin/activate

#Test the bot
python3 main.py

```

If successful, you should see "Bot started successfully!" in the logs.

## Create Systemd Service

Create the `pi_telegram_bot.service` in the directory as given below. Add the content from `pi-telegram-bot.service` to the file. Replace user `pi` with your username.
```bash
sudo nano /etc/systemd/system/pi-telegram-bot.service
```

Now enable and start the service.
```bash
sudo systemctl daemon-reload
sudo systemctl enable pi-telegram-bot
sudo systemctl start pi-telegram-bot
```

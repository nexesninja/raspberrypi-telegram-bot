### 1. Create a Telegram Bot  

Go to Telegram and search for `BotFather`.  
Start the bot by `/start` and send the command `/newbot`.  
Then provide a Name and username for the bot as instructed.  
Finally,save the bot_token given by BotFather. We need it later.  

### 2. Connecting rpi via SSH
  I have identified there are two ways of doing this in the internet. 
  But I will use the less complex way.

  
### 3. Setup a Virtual Environment

To install required packages,  
  ```
sudo apt update
sudo apt install python3-venv
```

Create a directory for Bot by,
```
mkdir -p ~/telegram_bot
```
Create the Virtual Environment by,
```
python3 -m venv ~/telegram_bot/venv
```
Then activate it by,
```
source ~/telegram_bot/venv/bin/activate
```
Install required packages by,
```
pip install python-telegram-bot
```

# Check Temperature
  This will guide you to setup the bot function script, Create the systemd service and troubleshooting. Things here are done by bash on a cmd by connecting rpi to computer via ssh. You can use GUI to to this too.

### 1. Set up the Bot Function
Create file temp.py in the bot directory.  
  
`nano ~/telegram_bot/temp.py`  
  
and paste the given code in temp.py in it.  
  
  
Now make the file executable using,  
  
`chmod +x ~/telegram_bot/temp.py`  
  

### 2. Create a Service  
Create a systemd service file.  
  
`sudo nano /etc/systemd/system/temp.service`  
  
then paste the content in temp.service to it.  

>MAKE SURE YOU CHANGE User=pi TO YOUR USERNAME AND CHANGE THE PATHS IN THE FILE TO SAME USERNAME USED. Also change bot_token to the token mentioned in prerequisities.
  
Save the file and Exit.  

Now the service can be enabled and started.  
  
    sudo systemctl daemon-reload
    sudo systemctl enable temp.service
    sudo systemctl start temp.service 
      
Run these commands seperately and you're good to go.  

### 3. Testing the Bot
Start your bot in Telegram by `/start`.    
You can,  
        1.Check Temperature by /temp  
        2.Get Help by /help (You can change what is shown by this command from the code)  

You can check if the service is running properly from the cmd too.  
`sudo systemctl status rpi-temp-bot.service`  



### 1. Create a Telegram Bot  

Go to Telegram and search for `BotFather`.  
Start the bot by `/start` and send the command `/newbot`.  
Then provide a Name and username for the bot as instructed.  
Finally,save the bot_token given by BotFather. We need it later.  

### 2. Connecting rpi via SSH  
  >This step is not necessary if you select GUI. You can find Youtube tutorials on this step.

  I have identified there are two ways of doing this in the internet. 
  But I will use the less complex way.
  
  First you need to [download](https://www.raspberrypi.com/software/) and install Raspberry Pi Imager.  
    
  Open the Imager and select your pi version, os and the device and click next.  
  In the dialog box appears, select `Edit Settings`.  

  Here, you should provide hostname, username and password wireless LAN Info.  
  Then head to services, Enable SSH and choose Use password authentication.
  Then you can continue the setup.  

  Now, after you intert your SD card into rpi and turned it on, it will be automatically connected to the WLAN.  
  Connect your computer to same WLAN and open command prompt.  

  To continue you have to know the IP Address of rpi. For that, you can use Fing on mobile or NMap from the desktop.  

  Now you can you following command to use the terminal of rpi.  
  ```ssh [username]@[ipaddress]```  

  Change [username] to username you gave in the setup and  [ipaddress] to the IP Address of rpi.  

  You will be asked for confirmation, type yes and click enter.
  
  
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

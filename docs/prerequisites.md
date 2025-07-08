# ✅ Prerequisites
  Before running the Telegram Bot on your Raspberry Pi 5, make sure you complete the following steps.

## 1️⃣ Create a Telegram Bot  

1. Open **Telegram** and search for `@BotFather`.
2. Start the bot by `/start` and send the command `/newbot`.  
3. Follow the prompts to:
  - Give your bot a **name**.
  - Choose a **unique username** (must end in `bot`).  
4. After setup, save the bot_token given by BotFather. You'll need this token to connect your bot to rpi.

## 2️⃣ Connect rpi via SSH  
> ⚠️ You can skip this section if you're using a display + keyboard (GUI mode).  
> For beginners, YouTube tutorials can help guide you through this step.

  I have identified there are two ways of doing this in the internet. 
  But I will use the less complex way using **Raspberry Pi Imager**.

### 🖥️ Raspberry Pi Imager Setup
1. Download and install [Raspberry Pi Imager](https://www.raspberrypi.com/software/).

2. Open the Imager and:
  - Select your Pi model and OS
  - Select the SD card.
  - Click **Next** and then **Edit Settings**.

3. In the dialog box opened:
- Set a **hostname**, **username**, and **password**.
- Enter your **Wi-Fi SSID** and **password**.
- Head to **Services**, **Enable SSH** and choose "Use password authentication".
- Continue the setup and write the image to SD Card. 

### 🔌 Find IP Address
  1. Insert the SD card into your Raspberry Pi and power it on.  
  It will be automatically connected to the WLAN.  
  2. Make sure your **computer is connected to the same Wi-Fi network**.
  3. Find the Pi’s IP address using one of these:
  -   📱 **Fing app** (mobile)
  -   🖥️ **Nmap** (desktop)
  -   🖥️ Use command 'ping [hostname].local (Change [hostname] with hostname you gave)  
     Any other method preferred can be used.
  
### 🔐 SSH into Your Raspberry Pi
 1. Use the following command to connect:
```bash
  ssh [username]@[ipaddress]
```  
  Replace:
-   [username] → The username you set in Raspberry Pi Imager
-   [ip_address] → The IP you found above  

  Type yes for confirmation.
  
  
## 3️⃣ Setup a Virtual Environment
Once you're logged into your Pi:
### 🔄 Update and Install Python venv
```bash
sudo apt update
sudo apt install python3-venv
```

### 📁 Create thr Bot Directory
```bash
mkdir ~/pi_telegram_bot
cd ~/pi_telegram_bot
```
### 🧪 Set Up the Virtual Environment
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```
## Install Requirements
Download or create file `requirements.txt` and copy the details in `requirements.txt` in repo to file.  
Then run the following command.  
  
```bash
pip install -r requirements.txt
```
  
You're now ready to start building your Telegram bot!

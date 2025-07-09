<p align="center">
  <img src="https://github.com/user-attachments/assets/f2a5bb8a-992e-4e36-bb33-90855adc7dd3" />
</p>


<h1 align="center">Raspberry Pi Telegram Bot</h1>

A fully functional Telegram bot for Raspberry Pi (rpi) with features like:

- 🌡️ Temperature Monitoring
- 📊 System Monitoring
- 💻 Remote Command Execution
- 🔧 More features coming soon!

I’m using SSH to connect to my rpi from a computer (no display required).

## 🚀 Getting Started

Before continuing, please complete the the prerequisites:

- [Create a Telegram Bot](https://github.com/nexesninja/raspberrypi-telegram-bot/blob/main/docs/prerequisites.md#1%EF%B8%8F%E2%83%A3-create-a-telegram-bot)
- [Connect to Raspberry Pi via SSH](https://github.com/nexesninja/raspberrypi-telegram-bot/blob/main/docs/prerequisites.md#2%EF%B8%8F%E2%83%A3-connect-rpi-via-ssh)
- [Set up a Python Virtual Environment](https://github.com/nexesninja/raspberrypi-telegram-bot/blob/main/docs/prerequisites.md#3%EF%B8%8F%E2%83%A3-setup-a-virtual-environment)

👉 The complete file can be found from [here](https://github.com/nexesninja/raspberrypi-telegram-bot/blob/main/docs/prerequisites.md).

## 🔒 Security Highlights

- **User Authorization:**   Only whitelisted Telegram user IDs can access the bot.
- **Command Whitelist:**   Only predefined safe commands can be executed.
- **Input Validation:**   Commands are parsed and validated before execution.
- **Command Injection Protection:**   Blocks dangerous patterns and injection attempts.
- **Timeout Protection:**   Commands timeout after 30 seconds.
- **Restricted Environment:**   Commands run with limited PATH and safe working directory.
  
## 📁 Project Modules

### 🌡️ Temperature Monitoring
This module allows you to check the RPi's temperature using the Telegram bot.

### 📊 System Monitoring
`/system` and `/status` provide CPU, RAM, Disk usage info.

### 💻 Remote Command Execution
Run whitelisted shell commands safely via `/cmd <command>`.

## 🗂️ Commands

| Command | Description |
| --- | --- |
| `/start` | Welcome message |
| `/temp` | Check Raspberry Pi temperature |
| `/system` | Full system status |
| `/status` | Quick overview |
| `/cmd <cmd>` | Execute whitelisted shell command |
| `/help` | List available commands |

More features coming soon!

## 📌 Roadmap

- [x]  Temperature Monitoring
- [x]  CPU & Memory Usage Display
- [x]  Run Custom Shell Commands

<hr>

![GitHub release (latest by date)](https://img.shields.io/github/v/release/nexesninja/raspberrypi-telegram-bot)
![Platform](https://img.shields.io/badge/platform-Raspberry%20Pi-ff69b4)
![License](https://img.shields.io/github/license/nexesninja/raspberrypi-telegram-bot)




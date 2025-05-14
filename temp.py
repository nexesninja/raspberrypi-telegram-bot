#!/usr/bin/env python3

import logging
import os
import time
import sys
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Function to get CPU temperature
def get_cpu_temperature():
    try:
        # Read temperature from thermal zone
        with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
            temp = float(f.read()) / 1000.0
        return f"{temp:.1f}°C"
    except Exception as e:
        logger.error(f"Failed to read temperature: {e}")
        return "Error reading temperature"

# Define command handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        f"Hi {user.mention_html()}! I'm your Raspberry Pi temperature monitor bot.\n"
        f"Use /temp to get the current CPU temperature."
    )

async def temp_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send the current CPU temperature."""
    temperature = get_cpu_temperature()
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    await update.message.reply_text(f"🌡️ Raspberry Pi Temperature: {temperature}\n⏱️ Time: {current_time}")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text(
        "Available commands:\n"
        "/start - Start the bot\n"
        "/temp - Get current CPU temperature\n"
        "/help - Show this help message"
    )

def main() -> None:
    """Start the bot with a retry mechanism."""
    # Get API token from environment variable
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        logger.error("No token provided. Set the TELEGRAM_BOT_TOKEN environment variable.")
        return

    retry_count = 0
    max_retries = 10
    wait_time = 30  # seconds
    
    # Start with a delay to ensure network is ready
    logger.info(f"Starting with an initial delay of {wait_time} seconds...")
    time.sleep(wait_time)
    
    while retry_count < max_retries:
        try:
            logger.info(f"Attempting to start bot (attempt {retry_count + 1}/{max_retries})")
            
            # Create the Application
            application = Application.builder().token(token).build()

            # Add command handlers
            application.add_handler(CommandHandler("start", start))
            application.add_handler(CommandHandler("help", help_command))
            application.add_handler(CommandHandler("temp", temp_command))

            # Start the Bot - this will block until Ctrl+C is pressed
            logger.info("Bot starting...")
            application.run_polling()
            
            # If we get here after polling stops, break the retry loop
            break
            
        except Exception as e:
            retry_count += 1
            logger.error(f"Failed to start bot: {e}")
            
            if retry_count < max_retries:
                logger.info(f"Waiting {wait_time} seconds before retrying...")
                time.sleep(wait_time)
            else:
                logger.error(f"Failed to start bot after {max_retries} attempts")
                break

if __name__ == '__main__':
    logger.info("Starting Telegram temperature bot with retry mechanism")
    main()

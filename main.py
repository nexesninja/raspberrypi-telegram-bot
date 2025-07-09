# main.py
import logging
import asyncio
from datetime import datetime, timedelta
from typing import Dict
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.constants import ParseMode

# Import our modules
from modules.temperature_monitor import TemperatureMonitor
from modules.system_monitor import SystemMonitor
from modules.command_executor import CommandExecutor
from config.config import (
    BOT_TOKEN, AUTHORIZED_USERS, RATE_LIMIT, 
    LOG_LEVEL, LOG_FILE, TEMP_CRITICAL_THRESHOLD
)

# Configure logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class RaspberryPiBot:
    def __init__(self):
        self.temp_monitor = TemperatureMonitor()
        self.system_monitor = SystemMonitor()
        self.command_executor = CommandExecutor()
        self.user_last_command = {}  # Rate limiting
        self.alert_sent = {}  # Temperature alert tracking
        
    def is_user_authorized(self, user_id: int) -> bool:
        """Check if user is authorized to use the bot"""
        return user_id in AUTHORIZED_USERS
    
    def check_rate_limit(self, user_id: int) -> bool:
        """Check if user is within rate limit"""
        now = datetime.now()
        if user_id not in self.user_last_command:
            self.user_last_command[user_id] = []
        
        # Remove old entries (older than 1 minute)
        self.user_last_command[user_id] = [
            timestamp for timestamp in self.user_last_command[user_id]
            if now - timestamp < timedelta(minutes=1)
        ]
        
        # Check if under rate limit
        if len(self.user_last_command[user_id]) >= RATE_LIMIT:
            return False
        
        # Add current timestamp
        self.user_last_command[user_id].append(now)
        return True
    
    async def check_authorization(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
        """Check authorization and rate limiting"""
        user_id = update.effective_user.id
        
        if not self.is_user_authorized(user_id):
            await update.message.reply_text(
                "❌ **Access Denied**\n\nYou are not authorized to use this bot.",
                parse_mode=ParseMode.MARKDOWN
            )
            logger.warning(f"Unauthorized access attempt from user {user_id}")
            return False
        
        if not self.check_rate_limit(user_id):
            await update.message.reply_text(
                f"⏱️ **Rate Limited**\n\nToo many commands. Limit: {RATE_LIMIT} per minute.",
                parse_mode=ParseMode.MARKDOWN
            )
            return False
        
        return True
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        if not await self.check_authorization(update, context):
            return
        
        pi_info = self.system_monitor.get_raspberry_pi_info()
        model = pi_info.get('model', 'Unknown Raspberry Pi')
        
        welcome_msg = f"🤖 **Raspberry Pi Bot Started**\n\n"
        welcome_msg += f"📱 **Device:** {model}\n"
        welcome_msg += f"🕐 **Started:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        welcome_msg += "**Available Commands:**\n"
        welcome_msg += "• `/temp` - Temperature status\n"
        welcome_msg += "• `/system` - System status\n"
        welcome_msg += "• `/cmd <command>` - Execute command\n"
        welcome_msg += "• `/help` - Show help\n"
        welcome_msg += "• `/status` - Quick status check\n"
        
        await update.message.reply_text(welcome_msg, parse_mode=ParseMode.MARKDOWN)
    
    async def temperature_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /temp command"""
        if not await self.check_authorization(update, context):
            return
        
        try:
            report = self.temp_monitor.format_temperature_report()
            await update.message.reply_text(report, parse_mode=ParseMode.MARKDOWN)
        except Exception as e:
            logger.error(f"Error in temperature command: {e}")
            await update.message.reply_text(f"❌ Error getting temperature data: {str(e)}")
    
    async def system_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /system command"""
        if not await self.check_authorization(update, context):
            return
        
        try:
            report = self.system_monitor.format_system_report()
            await update.message.reply_text(report, parse_mode=ParseMode.MARKDOWN)
        except Exception as e:
            logger.error(f"Error in system command: {e}")
            await update.message.reply_text(f"❌ Error getting system data: {str(e)}")
    
    async def command_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /cmd command"""
        if not await self.check_authorization(update, context):
            return
        
        if not context.args:
            help_text = self.command_executor.get_common_commands_help()
            await update.message.reply_text(help_text, parse_mode=ParseMode.MARKDOWN)
            return
        
        command = ' '.join(context.args)
        
        try:
            # Show typing indicator
            await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
            
            result = self.command_executor.execute_command(command)
            response = self.command_executor.format_command_result(result)
            
            # Split long messages
            if len(response) > 4096:
                for i in range(0, len(response), 4096):
                    await update.message.reply_text(
                        response[i:i+4096], 
                        parse_mode=ParseMode.MARKDOWN
                    )
            else:
                await update.message.reply_text(response, parse_mode=ParseMode.MARKDOWN)
                
        except Exception as e:
            logger.error(f"Error executing command '{command}': {e}")
            await update.message.reply_text(f"❌ Error executing command: {str(e)}")
    
    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /status command - quick overview"""
        if not await self.check_authorization(update, context):
            return
        
        try:
            temp_status = self.temp_monitor.get_temperature_status()
            cpu_data = self.system_monitor.get_cpu_usage()
            mem_data = self.system_monitor.get_memory_usage()
            uptime_data = self.system_monitor.get_system_uptime()
            
            status_msg = "⚡ **Quick Status**\n\n"
            
            # Temperature
            if temp_status['cpu_temp']:
                temp_emoji = "🔥" if temp_status['critical'] else "⚠️" if temp_status['warning'] else "✅"
                status_msg += f"{temp_emoji} **Temp:** {temp_status['cpu_temp']:.1f}°C\n"
            
            # CPU
            if 'error' not in cpu_data:
                cpu_emoji = "⚠️" if cpu_data.get('warning') else "✅"
                status_msg += f"{cpu_emoji} **CPU:** {cpu_data['overall']:.1f}%\n"
            
            # Memory
            if 'error' not in mem_data:
                mem_emoji = "⚠️" if mem_data.get('warning') else "✅"
                status_msg += f"{mem_emoji} **Memory:** {mem_data['percent']:.1f}%\n"
            
            # Uptime
            if 'error' not in uptime_data:
                status_msg += f"⏱️ **Uptime:** {uptime_data['uptime_formatted']}\n"
            
            await update.message.reply_text(status_msg, parse_mode=ParseMode.MARKDOWN)
            
        except Exception as e:
            logger.error(f"Error in status command: {e}")
            await update.message.reply_text(f"❌ Error getting status: {str(e)}")
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        if not await self.check_authorization(update, context):
            return
        
        help_text = "🤖 **Raspberry Pi Bot Help**\n\n"
        help_text += "**Commands:**\n"
        help_text += "• `/start` - Start the bot\n"
        help_text += "• `/temp` - Get temperature report\n"
        help_text += "• `/system` - Get system resource report\n"
        help_text += "• `/status` - Quick status overview\n"
        help_text += "• `/cmd <command>` - Execute shell command\n"
        help_text += "• `/help` - Show this help\n\n"
        
        help_text += "**Security Features:**\n"
        help_text += f"• Command whitelist ({len(self.command_executor.get_allowed_commands())} allowed)\n"
        help_text += "• User authorization required\n"
        help_text += f"• Rate limiting ({RATE_LIMIT} commands/minute)\n"
        help_text += "• Command timeout (30 seconds)\n"
        help_text += "• Input validation and sanitization\n\n"
        
        help_text += "**Examples:**\n"
        help_text += "`/cmd ls -la`\n"
        help_text += "`/cmd df -h`\n"
        help_text += "`/cmd ps aux`\n"
        help_text += "`/cmd uptime`\n"
        
        await update.message.reply_text(help_text, parse_mode=ParseMode.MARKDOWN)
    
    async def unknown_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle unknown messages"""
        if not await self.check_authorization(update, context):
            return
        
        await update.message.reply_text(
            "❓ **Unknown Command**\n\nUse `/help` to see available commands.",
            parse_mode=ParseMode.MARKDOWN
        )
    
    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle errors"""
        logger.error(f"Update {update} caused error {context.error}")
        
        if update and update.message:
            await update.message.reply_text(
                "❌ **An error occurred**\n\nPlease try again later.",
                parse_mode=ParseMode.MARKDOWN
            )
    
    async def periodic_monitoring(self, context: ContextTypes.DEFAULT_TYPE):
        """Periodic monitoring and alerts"""
        try:
            temp_status = self.temp_monitor.get_temperature_status()
            
            # Temperature alerts
            if temp_status['critical'] and not self.alert_sent.get('temp_critical'):
                alert_msg = f"🚨 **CRITICAL TEMPERATURE ALERT**\n\n"
                alert_msg += f"CPU Temperature: {temp_status['cpu_temp']:.1f}°C\n"
                alert_msg += f"Threshold: {TEMP_CRITICAL_THRESHOLD}°C\n\n"
                alert_msg += "Please check cooling and reduce load!"
                
                for user_id in AUTHORIZED_USERS:
                    try:
                        await context.bot.send_message(
                            chat_id=user_id,
                            text=alert_msg,
                            parse_mode=ParseMode.MARKDOWN
                        )
                    except Exception as e:
                        logger.error(f"Failed to send alert to {user_id}: {e}")
                
                self.alert_sent['temp_critical'] = True
            elif not temp_status['critical']:
                self.alert_sent['temp_critical'] = False
                
        except Exception as e:
            logger.error(f"Error in periodic monitoring: {e}")
    
    def run(self):
        """Run the bot"""
        if not BOT_TOKEN or BOT_TOKEN == 'YOUR_BOT_TOKEN_HERE':
            logger.error("Bot token not configured. Please set BOT_TOKEN in config/config.py")
            return
        
        if not AUTHORIZED_USERS:
            logger.error("No authorized users configured. Please add user IDs to AUTHORIZED_USERS in config/config.py")
            return
        
        logger.info("Starting Raspberry Pi Telegram Bot...")
        
        # Create application
        application = Application.builder().token(BOT_TOKEN).build()
        
        # Add handlers
        application.add_handler(CommandHandler("start", self.start_command))
        application.add_handler(CommandHandler("temp", self.temperature_command))
        application.add_handler(CommandHandler("system", self.system_command))
        application.add_handler(CommandHandler("cmd", self.command_handler))
        application.add_handler(CommandHandler("status", self.status_command))
        application.add_handler(CommandHandler("help", self.help_command))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.unknown_command))
        
        # Add error handler
        application.add_error_handler(self.error_handler)
        
        # Add periodic monitoring job (every 5 minutes)
        job_queue = application.job_queue
        job_queue.run_repeating(self.periodic_monitoring, interval=300, first=60)
        
        logger.info("Bot started successfully!")
        
        # Run the bot
        application.run_polling(allowed_updates=Update.ALL_TYPES)

def main():
    """Main function"""
    bot = RaspberryPiBot()
    bot.run()

if __name__ == '__main__':
    main()

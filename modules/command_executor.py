# modules/command_executor.py
import subprocess
import shlex
import logging
import re
from typing import Dict, List, Tuple
from config.config import ALLOWED_COMMANDS

logger = logging.getLogger(__name__)

class CommandExecutor:
    def __init__(self):
        self.max_output_length = 4000  # Telegram message limit consideration
        self.timeout = 30  # Command timeout in seconds
        
    def is_command_allowed(self, command: str) -> Tuple[bool, str]:
        """Check if command is in whitelist and safe to execute"""
        if not command.strip():
            return False, "Empty command"
        
        # Parse command to get the base command
        try:
            args = shlex.split(command)
        except ValueError as e:
            return False, f"Invalid command syntax: {e}"
        
        if not args:
            return False, "No command provided"
        
        base_command = args[0]
        
        # Check if base command is in whitelist
        if base_command not in ALLOWED_COMMANDS:
            return False, f"Command '{base_command}' not allowed"
        
        # Additional security checks
        dangerous_patterns = [
            r'rm\s+-rf\s+/',  # Dangerous rm commands
            r'>\s*/dev/',     # Writing to device files
            r'mkfs',          # Format filesystem
            r'fdisk',         # Disk partitioning
            r'dd\s+.*of=',    # Dangerous dd operations
            r'chmod\s+777',   # Overly permissive permissions
            r'passwd',        # Password changes
            r'su\s+',         # Switch user
            r'sudo\s+',       # Sudo commands (if you want to block them)
            r'\|.*rm',        # Piped rm commands
            r'&.*rm',         # Background rm commands
        ]
        
        for pattern in dangerous_patterns:
            if re.search(pattern, command, re.IGNORECASE):
                return False, f"Command contains dangerous pattern: {pattern}"
        
        # Check for command injection attempts
        injection_chars = [';', '&&', '||', '`', '$()']
        for char in injection_chars:
            if char in command and base_command not in ['grep', 'find']:  # grep and find may legitimately use some of these
                return False, f"Command injection attempt detected: {char}"
        
        return True, "Command allowed"
    
    def execute_command(self, command: str) -> Dict:
        """Execute a command safely with security checks"""
        # Security check
        allowed, reason = self.is_command_allowed(command)
        if not allowed:
            logger.warning(f"Blocked command execution: {command} - Reason: {reason}")
            return {
                'success': False,
                'error': f"Security check failed: {reason}",
                'command': command
            }
        
        try:
            logger.info(f"Executing command: {command}")
            
            # Execute command with timeout and security restrictions
            result = subprocess.run(
                shlex.split(command),
                capture_output=True,
                text=True,
                timeout=self.timeout,
                cwd='/home/pi',  # Set safe working directory
                env={'PATH': '/usr/local/bin:/usr/bin:/bin'},  # Restricted PATH
                shell=False  # Never use shell=True for security
            )
            
            # Prepare output
            stdout = result.stdout
            stderr = result.stderr
            
            # Truncate output if too long
            if len(stdout) > self.max_output_length:
                stdout = stdout[:self.max_output_length] + "\n... (output truncated)"
            
            if len(stderr) > self.max_output_length:
                stderr = stderr[:self.max_output_length] + "\n... (error output truncated)"
            
            return {
                'success': result.returncode == 0,
                'return_code': result.returncode,
                'stdout': stdout,
                'stderr': stderr,
                'command': command
            }
            
        except subprocess.TimeoutExpired:
            logger.warning(f"Command timed out: {command}")
            return {
                'success': False,
                'error': f"Command timed out after {self.timeout} seconds",
                'command': command
            }
        except subprocess.CalledProcessError as e:
            logger.error(f"Command failed: {command} - Error: {e}")
            return {
                'success': False,
                'error': f"Command failed with return code {e.returncode}",
                'stderr': e.stderr if hasattr(e, 'stderr') else '',
                'command': command
            }
        except Exception as e:
            logger.error(f"Unexpected error executing command: {command} - Error: {e}")
            return {
                'success': False,
                'error': f"Unexpected error: {str(e)}",
                'command': command
            }
    
    def get_allowed_commands(self) -> List[str]:
        """Get list of allowed commands"""
        return ALLOWED_COMMANDS.copy()
    
    def format_command_result(self, result: Dict) -> str:
        """Format command execution result for display"""
        if not result.get('success'):
            message = f"❌ **Command Failed**\n"
            message += f"**Command:** `{result.get('command', 'unknown')}`\n"
            message += f"**Error:** {result.get('error', 'Unknown error')}\n"
            
            if result.get('stderr'):
                message += f"**Error Output:**\n```\n{result['stderr']}\n```"
            
            return message
        
        message = f"✅ **Command Executed Successfully**\n"
        message += f"**Command:** `{result.get('command', 'unknown')}`\n"
        
        if result.get('return_code') is not None:
            message += f"**Return Code:** {result['return_code']}\n"
        
        if result.get('stdout'):
            message += f"**Output:**\n```\n{result['stdout']}\n```"
        
        if result.get('stderr'):
            message += f"**Warnings:**\n```\n{result['stderr']}\n```"
        
        return message
    
    def get_common_commands_help(self) -> str:
        """Get help text with common useful commands"""
        help_text = "🔧 **Available Commands**\n\n"
        help_text += "**System Information:**\n"
        help_text += "• `uname -a` - System information\n"
        help_text += "• `lscpu` - CPU information\n"
        help_text += "• `free -h` - Memory usage\n"
        help_text += "• `df -h` - Disk usage\n"
        help_text += "• `uptime` - System uptime\n\n"
        
        help_text += "**Process Management:**\n"
        help_text += "• `ps aux` - Running processes\n"
        help_text += "• `top -b -n1` - Process snapshot\n"
        help_text += "• `systemctl status` - Service status\n\n"
        
        help_text += "**File Operations:**\n"
        help_text += "• `ls -la` - List files\n"
        help_text += "• `pwd` - Current directory\n"
        help_text += "• `cat /proc/cpuinfo` - CPU details\n"
        help_text += "• `tail -f /var/log/syslog` - System log\n\n"
        
        help_text += "**Network:**\n"
        help_text += "• `ping -c 4 google.com` - Network test\n"
        help_text += "• `wget --spider google.com` - Connection test\n\n"
        
        help_text += f"**Security:** Only {len(ALLOWED_COMMANDS)} whitelisted commands allowed.\n"
        help_text += "**Timeout:** Commands timeout after 30 seconds.\n"
        
        return help_text

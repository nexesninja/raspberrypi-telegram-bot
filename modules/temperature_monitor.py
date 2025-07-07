# modules/temperature_monitor.py
import subprocess
import logging
from typing import Dict, Optional
from config.config import TEMP_WARNING_THRESHOLD, TEMP_CRITICAL_THRESHOLD

logger = logging.getLogger(__name__)

class TemperatureMonitor:
    def __init__(self):
        self.last_temp = 0.0
        
    def get_cpu_temperature(self) -> Optional[float]:
        """Get CPU temperature from vcgencmd or thermal zone"""
        try:
            # Try vcgencmd first (Raspberry Pi specific)
            result = subprocess.run(
                ['vcgencmd', 'measure_temp'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                temp_str = result.stdout.strip()
                # Extract temperature from "temp=XX.X'C"
                temp = float(temp_str.split('=')[1].split("'")[0])
                return temp
        except (subprocess.TimeoutExpired, subprocess.CalledProcessError, ValueError, IndexError):
            pass
            
        try:
            # Fallback to thermal zone
            with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
                temp_millidegrees = int(f.read().strip())
                temp = temp_millidegrees / 1000.0
                return temp
        except (FileNotFoundError, ValueError, PermissionError):
            pass
            
        logger.error("Unable to read CPU temperature")
        return None
    
    def get_gpu_temperature(self) -> Optional[float]:
        """Get GPU temperature (Raspberry Pi specific)"""
        try:
            result = subprocess.run(
                ['vcgencmd', 'measure_temp', 'gpu'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                temp_str = result.stdout.strip()
                temp = float(temp_str.split('=')[1].split("'")[0])
                return temp
        except (subprocess.TimeoutExpired, subprocess.CalledProcessError, ValueError, IndexError):
            pass
        return None
    
    def get_temperature_status(self) -> Dict:
        """Get comprehensive temperature status"""
        cpu_temp = self.get_cpu_temperature()
        gpu_temp = self.get_gpu_temperature()
        
        status = {
            'cpu_temp': cpu_temp,
            'gpu_temp': gpu_temp,
            'status': 'unknown',
            'warning': False,
            'critical': False
        }
        
        if cpu_temp is not None:
            self.last_temp = cpu_temp
            
            if cpu_temp >= TEMP_CRITICAL_THRESHOLD:
                status['status'] = 'critical'
                status['critical'] = True
                status['warning'] = True
            elif cpu_temp >= TEMP_WARNING_THRESHOLD:
                status['status'] = 'warning'
                status['warning'] = True
            else:
                status['status'] = 'normal'
        
        return status
    
    def get_thermal_throttling_status(self) -> Dict:
        """Check thermal throttling status"""
        try:
            result = subprocess.run(
                ['vcgencmd', 'get_throttled'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                throttled_hex = result.stdout.strip().split('=')[1]
                throttled_int = int(throttled_hex, 16)
                
                return {
                    'raw_value': throttled_hex,
                    'under_voltage_detected': bool(throttled_int & 0x1),
                    'arm_frequency_capped': bool(throttled_int & 0x2),
                    'currently_throttled': bool(throttled_int & 0x4),
                    'soft_temperature_limit': bool(throttled_int & 0x8),
                    'under_voltage_occurred': bool(throttled_int & 0x10000),
                    'arm_frequency_capped_occurred': bool(throttled_int & 0x20000),
                    'throttling_occurred': bool(throttled_int & 0x40000),
                    'soft_temperature_limit_occurred': bool(throttled_int & 0x80000)
                }
        except (subprocess.TimeoutExpired, subprocess.CalledProcessError, ValueError, IndexError):
            pass
        
        return {}
    
    def format_temperature_report(self) -> str:
        """Format a comprehensive temperature report"""
        temp_status = self.get_temperature_status()
        throttle_status = self.get_thermal_throttling_status()
        
        report = "🌡️ **Temperature Report**\n\n"
        
        if temp_status['cpu_temp'] is not None:
            cpu_temp = temp_status['cpu_temp']
            temp_emoji = "🔥" if temp_status['critical'] else "⚠️" if temp_status['warning'] else "✅"
            report += f"{temp_emoji} **CPU Temperature:** {cpu_temp:.1f}°C\n"
        
        if temp_status['gpu_temp'] is not None:
            report += f"🎮 **GPU Temperature:** {temp_status['gpu_temp']:.1f}°C\n"
        
        report += f"📊 **Status:** {temp_status['status'].upper()}\n\n"
        
        if throttle_status:
            report += "🔧 **Throttling Status:**\n"
            if throttle_status.get('currently_throttled'):
                report += "⚠️ Currently throttled\n"
            if throttle_status.get('under_voltage_detected'):
                report += "⚠️ Under voltage detected\n"
            if throttle_status.get('arm_frequency_capped'):
                report += "⚠️ ARM frequency capped\n"
            if throttle_status.get('soft_temperature_limit'):
                report += "⚠️ Soft temperature limit active\n"
            
            if not any([throttle_status.get('currently_throttled'),
                       throttle_status.get('under_voltage_detected'),
                       throttle_status.get('arm_frequency_capped'),
                       throttle_status.get('soft_temperature_limit')]):
                report += "✅ No current throttling\n"
        
        return report

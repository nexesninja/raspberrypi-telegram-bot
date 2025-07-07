# modules/system_monitor.py
import psutil
import subprocess
import logging
from typing import Dict, List
from datetime import datetime, timedelta
from config.config import CPU_WARNING_THRESHOLD, MEMORY_WARNING_THRESHOLD

logger = logging.getLogger(__name__)

class SystemMonitor:
    def __init__(self):
        self.boot_time = datetime.fromtimestamp(psutil.boot_time())
        
    def get_cpu_usage(self) -> Dict:
        """Get CPU usage statistics"""
        try:
            # Get CPU usage per core and overall
            cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
            cpu_overall = psutil.cpu_percent(interval=0)
            cpu_freq = psutil.cpu_freq()
            cpu_count = psutil.cpu_count()
            
            return {
                'overall': cpu_overall,
                'per_core': cpu_percent,
                'cores': cpu_count,
                'frequency': {
                    'current': cpu_freq.current if cpu_freq else None,
                    'min': cpu_freq.min if cpu_freq else None,
                    'max': cpu_freq.max if cpu_freq else None
                },
                'warning': cpu_overall >= CPU_WARNING_THRESHOLD
            }
        except Exception as e:
            logger.error(f"Error getting CPU usage: {e}")
            return {'error': str(e)}
    
    def get_memory_usage(self) -> Dict:
        """Get memory usage statistics"""
        try:
            memory = psutil.virtual_memory()
            swap = psutil.swap_memory()
            
            return {
                'total': memory.total,
                'available': memory.available,
                'used': memory.used,
                'free': memory.free,
                'percent': memory.percent,
                'swap_total': swap.total,
                'swap_used': swap.used,
                'swap_free': swap.free,
                'swap_percent': swap.percent,
                'warning': memory.percent >= MEMORY_WARNING_THRESHOLD
            }
        except Exception as e:
            logger.error(f"Error getting memory usage: {e}")
            return {'error': str(e)}
    
    def get_disk_usage(self) -> Dict:
        """Get disk usage statistics"""
        try:
            disk_usage = {}
            partitions = psutil.disk_partitions()
            
            for partition in partitions:
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    disk_usage[partition.mountpoint] = {
                        'device': partition.device,
                        'fstype': partition.fstype,
                        'total': usage.total,
                        'used': usage.used,
                        'free': usage.free,
                        'percent': (usage.used / usage.total) * 100
                    }
                except PermissionError:
                    continue
            
            return disk_usage
        except Exception as e:
            logger.error(f"Error getting disk usage: {e}")
            return {'error': str(e)}
    
    def get_network_stats(self) -> Dict:
        """Get network statistics"""
        try:
            net_io = psutil.net_io_counters()
            net_connections = len(psutil.net_connections())
            
            return {
                'bytes_sent': net_io.bytes_sent,
                'bytes_recv': net_io.bytes_recv,
                'packets_sent': net_io.packets_sent,
                'packets_recv': net_io.packets_recv,
                'connections': net_connections
            }
        except Exception as e:
            logger.error(f"Error getting network stats: {e}")
            return {'error': str(e)}
    
    def get_system_uptime(self) -> Dict:
        """Get system uptime"""
        try:
            uptime = datetime.now() - self.boot_time
            return {
                'boot_time': self.boot_time,
                'uptime_seconds': uptime.total_seconds(),
                'uptime_formatted': str(uptime).split('.')[0]
            }
        except Exception as e:
            logger.error(f"Error getting uptime: {e}")
            return {'error': str(e)}
    
    def get_top_processes(self, limit: int = 5) -> List[Dict]:
        """Get top processes by CPU and memory usage"""
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'username']):
                try:
                    processes.append(proc.info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            
            # Sort by CPU usage
            processes.sort(key=lambda x: x['cpu_percent'] or 0, reverse=True)
            return processes[:limit]
        except Exception as e:
            logger.error(f"Error getting top processes: {e}")
            return []
    
    def get_raspberry_pi_info(self) -> Dict:
        """Get Raspberry Pi specific information"""
        info = {}
        
        try:
            # Get model information
            with open('/proc/device-tree/model', 'r') as f:
                info['model'] = f.read().strip().replace('\x00', '')
        except FileNotFoundError:
            pass
        
        try:
            # Get firmware version
            result = subprocess.run(['vcgencmd', 'version'], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                info['firmware'] = result.stdout.strip().split('\n')[0]
        except (subprocess.TimeoutExpired, subprocess.CalledProcessError):
            pass
        
        try:
            # Get memory split
            result = subprocess.run(['vcgencmd', 'get_mem', 'arm'], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                info['arm_memory'] = result.stdout.strip()
            
            result = subprocess.run(['vcgencmd', 'get_mem', 'gpu'], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                info['gpu_memory'] = result.stdout.strip()
        except (subprocess.TimeoutExpired, subprocess.CalledProcessError):
            pass
        
        return info
    
    def format_system_report(self) -> str:
        """Format a comprehensive system report"""
        report = "💻 **System Status Report**\n\n"
        
        # CPU Usage
        cpu_data = self.get_cpu_usage()
        if 'error' not in cpu_data:
            cpu_emoji = "⚠️" if cpu_data.get('warning') else "✅"
            report += f"{cpu_emoji} **CPU Usage:** {cpu_data['overall']:.1f}%\n"
            report += f"🔧 **Cores:** {cpu_data['cores']}\n"
            if cpu_data['frequency']['current']:
                report += f"⚡ **Frequency:** {cpu_data['frequency']['current']:.0f} MHz\n"
        
        # Memory Usage
        mem_data = self.get_memory_usage()
        if 'error' not in mem_data:
            mem_emoji = "⚠️" if mem_data.get('warning') else "✅"
            mem_gb = mem_data['used'] / (1024**3)
            mem_total_gb = mem_data['total'] / (1024**3)
            report += f"{mem_emoji} **Memory:** {mem_gb:.1f}/{mem_total_gb:.1f} GB ({mem_data['percent']:.1f}%)\n"
            
            if mem_data['swap_total'] > 0:
                swap_gb = mem_data['swap_used'] / (1024**3)
                swap_total_gb = mem_data['swap_total'] / (1024**3)
                report += f"💾 **Swap:** {swap_gb:.1f}/{swap_total_gb:.1f} GB ({mem_data['swap_percent']:.1f}%)\n"
        
        # Disk Usage
        disk_data = self.get_disk_usage()
        if 'error' not in disk_data and disk_data:
            report += "\n💽 **Disk Usage:**\n"
            for mount, data in disk_data.items():
                if mount in ['/', '/boot']:  # Show main partitions
                    used_gb = data['used'] / (1024**3)
                    total_gb = data['total'] / (1024**3)
                    report += f"  {mount}: {used_gb:.1f}/{total_gb:.1f} GB ({data['percent']:.1f}%)\n"
        
        # Uptime
        uptime_data = self.get_system_uptime()
        if 'error' not in uptime_data:
            report += f"\n⏱️ **Uptime:** {uptime_data['uptime_formatted']}\n"
        
        # Top Processes
        top_procs = self.get_top_processes(3)
        if top_procs:
            report += "\n🔝 **Top Processes:**\n"
            for proc in top_procs:
                cpu_pct = proc['cpu_percent'] or 0
                mem_pct = proc['memory_percent'] or 0
                report += f"  {proc['name']}: CPU {cpu_pct:.1f}%, MEM {mem_pct:.1f}%\n"
        
        return report
    
    def format_bytes(self, bytes_val: int) -> str:
        """Format bytes to human readable format"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_val < 1024:
                return f"{bytes_val:.1f} {unit}"
            bytes_val /= 1024
        return f"{bytes_val:.1f} PB"

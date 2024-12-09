import psutil
import platform
import GPUtil
from datetime import datetime
from ..core.logger import log_to_console, log_error

def get_size(bytes):
    """Конвертує байти в читабельний формат"""
    try:
        for unit in ['', 'K', 'M', 'G', 'T', 'P']:
            if bytes < 1024:
                return f"{bytes:.2f}{unit}B"
            bytes /= 1024
    except Exception as e:
        log_error("Error converting bytes to readable format", e)
        return "0B"

def get_system_info():
    """Отримати системну інформацію"""
    try:
        log_to_console("Starting system information collection")
        info = []
        
        # Загальна інформація про систему
        log_to_console("Collecting general system information")
        system_info = {
            'system': platform.system(),
            'version': platform.version(),
            'processor': platform.processor(),
            'node': platform.node()
        }
        info.append("🖥️ *Система:*")
        info.append(f"• OS: `{system_info['system']} {system_info['version']}`")
        info.append(f"• Процесор: `{system_info['processor']}`")
        info.append(f"• Ім'я комп'ютера: `{system_info['node']}`")
        info.append("")

        # CPU
        log_to_console("Collecting CPU information")
        cpu_freq = psutil.cpu_freq()
        cpu_info = {
            'percent': psutil.cpu_percent(),
            'freq': cpu_freq.current,
            'cores': psutil.cpu_count()
        }
        info.append("💻 *Процесор:*")
        info.append(f"• Використання: `{cpu_info['percent']}%`")
        info.append(f"• Частота: `{cpu_info['freq']:.2f}MHz`")
        info.append(f"• Ядра: `{cpu_info['cores']}`")
        info.append("")

        # Пам'ять
        log_to_console("Collecting memory information")
        memory = psutil.virtual_memory()
        memory_info = {
            'total': get_size(memory.total),
            'used': get_size(memory.used),
            'percent': memory.percent,
            'available': get_size(memory.available)
        }
        info.append("📝 *Оперативна пам'ять:*")
        info.append(f"• Всього: `{memory_info['total']}`")
        info.append(f"• Використано: `{memory_info['used']} ({memory_info['percent']}%)`")
        info.append(f"• Доступно: `{memory_info['available']}`")
        info.append("")

        # Диски
        log_to_console("Collecting disk information")
        info.append("💾 *Диски:*")
        partitions = psutil.disk_partitions()
        for partition in partitions:
            try:
                partition_usage = psutil.disk_usage(partition.mountpoint)
                disk_info = {
                    'device': partition.device,
                    'total': get_size(partition_usage.total),
                    'used': get_size(partition_usage.used),
                    'percent': partition_usage.percent,
                    'free': get_size(partition_usage.free)
                }
                info.append(f"*Диск {disk_info['device']}:*")
                info.append(f"  • Всього: `{disk_info['total']}`")
                info.append(f"  • Використано: `{disk_info['used']} ({disk_info['percent']}%)`")
                info.append(f"  • Вільно: `{disk_info['free']}`")
                log_to_console(f"Collected information for disk {partition.device}")
            except Exception as e:
                log_error(f"Error collecting information for disk {partition.device}", e)
                continue
        info.append("")

        # GPU
        try:
            log_to_console("Collecting GPU information")
            gpus = GPUtil.getGPUs()
            if gpus:
                info.append("🎮 *Відеокарта:*")
                for gpu in gpus:
                    gpu_info = {
                        'name': gpu.name,
                        'load': gpu.load * 100,
                        'memory_used': gpu.memoryUsed,
                        'memory_total': gpu.memoryTotal,
                        'temperature': gpu.temperature
                    }
                    info.append(f"• Модель: `{gpu_info['name']}`")
                    info.append(f"• Використання: `{gpu_info['load']:.1f}%`")
                    info.append(f"• Пам'ять: `{gpu_info['memory_used']}MB/{gpu_info['memory_total']}MB`")
                    info.append(f"• Температура: `{gpu_info['temperature']}°C`")
                    log_to_console(f"Collected information for GPU: {gpu.name}")
                info.append("")
        except Exception as e:
            log_error("Error collecting GPU information", e)
            log_to_console("GPU information collection skipped", "WARNING")

        # Мережа
        try:
            log_to_console("Collecting network information")
            network = psutil.net_io_counters()
            network_info = {
                'sent': get_size(network.bytes_sent),
                'received': get_size(network.bytes_recv)
            }
            info.append("🌐 *Мережа:*")
            info.append(f"• Відправлено: `{network_info['sent']}`")
            info.append(f"• Отримано: `{network_info['received']}`")
        except Exception as e:
            log_error("Error collecting network information", e)
            log_to_console("Network information collection skipped", "WARNING")
        
        log_to_console("System information collection completed successfully")
        return "\n".join(info)
    except Exception as e:
        error_msg = f"Помилка отримання системної інформації: {str(e)}"
        log_error("Critical error collecting system information", e)
        return error_msg 
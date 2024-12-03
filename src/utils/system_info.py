import psutil
import platform
import GPUtil
from datetime import datetime

def get_size(bytes):
    """Конвертує байти в читабельний формат"""
    for unit in ['', 'K', 'M', 'G', 'T', 'P']:
        if bytes < 1024:
            return f"{bytes:.2f}{unit}B"
        bytes /= 1024

def get_system_info():
    try:
        info = []
        
        # Загальна інформація про систему
        info.append("🖥️ *Система:*")
        info.append(f"• OS: `{platform.system()} {platform.version()}`")
        info.append(f"• Процесор: `{platform.processor()}`")
        info.append(f"• Ім'я комп'ютера: `{platform.node()}`")
        info.append("")

        # CPU
        cpu_freq = psutil.cpu_freq()
        info.append("💻 *Процесор:*")
        info.append(f"• Використання: `{psutil.cpu_percent()}%`")
        info.append(f"• Частота: `{cpu_freq.current:.2f}MHz`")
        info.append(f"• Ядра: `{psutil.cpu_count()}`")
        info.append("")

        # Пам'ять
        memory = psutil.virtual_memory()
        info.append("📝 *Оперативна пам'ять:*")
        info.append(f"• Всього: `{get_size(memory.total)}`")
        info.append(f"• Використано: `{get_size(memory.used)} ({memory.percent}%)`")
        info.append(f"• Доступно: `{get_size(memory.available)}`")
        info.append("")

        # Диски
        info.append("💾 *Диски:*")
        partitions = psutil.disk_partitions()
        for partition in partitions:
            try:
                partition_usage = psutil.disk_usage(partition.mountpoint)
                info.append(f"*Диск {partition.device}:*")
                info.append(f"  • Всього: `{get_size(partition_usage.total)}`")
                info.append(f"  • Використано: `{get_size(partition_usage.used)} ({partition_usage.percent}%)`")
                info.append(f"  • Вільно: `{get_size(partition_usage.free)}`")
            except:
                continue
        info.append("")

        # GPU
        try:
            gpus = GPUtil.getGPUs()
            if gpus:
                info.append("🎮 *Відеокарта:*")
                for gpu in gpus:
                    info.append(f"• Модель: `{gpu.name}`")
                    info.append(f"• Використання: `{gpu.load*100:.1f}%`")
                    info.append(f"• Пам'ять: `{gpu.memoryUsed}MB/{gpu.memoryTotal}MB`")
                    info.append(f"• Температура: `{gpu.temperature}°C`")
                info.append("")
        except:
            pass

        # Мережа
        network = psutil.net_io_counters()
        info.append("🌐 *Мережа:*")
        info.append(f"• Відправлено: `{get_size(network.bytes_sent)}`")
        info.append(f"• Отримано: `{get_size(network.bytes_recv)}`")
        
        return "\n".join(info)
    except Exception as e:
        return f"Помилка отримання системної інформації: {str(e)}" 
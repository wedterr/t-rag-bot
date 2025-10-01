import platform
from ppycron.src import UnixInterface, WindowsInterface

python_script = "update_index.py"
cron_schedule = "30 2 * * *"  # запуск каждый день в 2:30

if platform.system() == "Windows":
    interface = WindowsInterface()
else:
    interface = UnixInterface()

# Добавляем задачу обновления индекса
task = interface.add(
    command=f"python {python_script}",
    interval=cron_schedule
)

print(f"Добавлено задание с ID: {task.id}")
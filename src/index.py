import os
import subprocess
import threading
import webview
import ctypes
from time import time
from datetime import datetime
import psutil
import screen_brightness_control as sbc
import time
import gpustat

CPU_IDLE_POWER = 90
GPU_IDLE_POWER = 3
DISK_IDLE_POWER = 7
DISPLAY_IDLE_POWER = 100

def get_total_ram_power():
    total_ram_gb = psutil.virtual_memory().total / (1024 ** 3)  # Convert bytes to GB
    ram_power_per_gb = 0.375 # rough estimate
    total_ram_power = total_ram_gb * ram_power_per_gb
    return total_ram_power


def get_display_brightness():
    try:
        brightness = sbc.get_brightness(display=0)
        if brightness:
            return brightness[0]
    except Exception as e:
        print(f"Could not get display brightness: {e}")
    return 50

def get_gpu_utilization():
    try:
        gpu_stats = gpustat.GPUStatCollection.new_query()
        total_utilization = sum(gpu.utilization for gpu in gpu_stats.gpus)
        gpu_count = len(gpu_stats.gpus)
        return total_utilization / gpu_count if gpu_count > 0 else 0  # Average utilization of all GPUs
    except Exception as e:
        print(f"Could not get GPU utilization: {e}")
    return 0

def get_ram_percentage():
    return psutil.virtual_memory()[2]

def get_cpu_percentage():
    return psutil.cpu_percent(4)

def get_disk_percentage():
    try:
        drive_str = subprocess.check_output("fsutil fsinfo drives").strip().lstrip(b'Drives: ')
        drives = drive_str.split()
        total_usage = sum(psutil.disk_usage(drive.decode()).percent for drive in drives)
        num_drives = len(drives)
        return total_usage / num_drives if num_drives > 0 else 0
    except Exception as e:
        print(f"Error occurred: {e}")
        return None


def estimate_power_consumption():
    cpu_percent = get_cpu_percentage()
    disk_percent = get_disk_percentage()
    gpu_percent = get_gpu_utilization()

    ram_percent = get_ram_percentage()
    total_ram_power = get_total_ram_power()

    display_brightness = get_display_brightness()

    cpu_power = CPU_IDLE_POWER + (cpu_percent / 100) * CPU_IDLE_POWER
    gpu_power = GPU_IDLE_POWER + (gpu_percent / 100) * GPU_IDLE_POWER
    ram_power = (ram_percent / 100) * total_ram_power
    disk_power = DISK_IDLE_POWER + (disk_percent / 100) * DISK_IDLE_POWER
    display_power = display_brightness + (display_brightness / 100) * display_brightness

    total_power = cpu_power + gpu_power + ram_power  + display_power
    return total_power



def get_carbon_intensity_data(country):
    url = "https://jsonplaceholder.typicode.com/posts/1"
    response = requests.get(url)
    response_json = response.json()

    return response_json

def calculate_carbon_emmission():
    power_consumption_w = estimate_power_consumption()
    carbon_intensity_kg_co2_per_kwh =  0.475

    power_consumption_kwh = power_consumption_w / 1000

    carbon_emissions_kg_co2 = (power_consumption_kwh * carbon_intensity_kg_co2_per_kwh) / 3600

    return carbon_emissions_kg_co2


def get_computer_uptime():
    lib = ctypes.windll.kernel32
    t = lib.GetTickCount64()
    t = int(str(t)[:-3])

    mins, sec = divmod(t, 60)
    hour, mins = divmod(mins, 60)
    days, hour = divmod(hour, 24)

    return [days, hour, mins, sec]

def save_statistics(dirloc, data):
    timestamp = datetime.now().timestamp()

    with open(f"{dirloc}/{int(timestamp)}", 'w') as f:
        f.write(data)


class Api:
    def fullscreen(self):
        webview.windows[0].toggle_fullscreen()

    def save_content(self, content):
        filename = webview.windows[0].create_file_dialog(webview.SAVE_DIALOG)
        if not filename:
            return

        with open(filename, 'w') as f:
            f.write(content)

    def get_data(self):
        return {
            "computer_uptime": get_computer_uptime(),
            "carbon_emmision": calculate_carbon_emmission()
        }


    def ls(self):
        return os.listdir('.')


def get_entrypoint():
    def exists(path):
        return os.path.exists(os.path.join(os.path.dirname(__file__), path))

    if exists('../gui/index.html'): # unfrozen development
        return '../gui/index.html'

    if exists('../Resources/gui/index.html'): # frozen py2app
        return '../Resources/gui/index.html'

    if exists('./gui/index.html'):
        return './gui/index.html'

    raise Exception('No index.html found')


def set_interval(interval):
    def decorator(function):
        def wrapper(*args, **kwargs):
            stopped = threading.Event()

            def loop(): # executed in another thread
                while not stopped.wait(interval): # until stopped
                    function(*args, **kwargs)

            t = threading.Thread(target=loop)
            t.daemon = True # stop if the program exits
            t.start()
            return stopped
        return wrapper
    return decorator



entry = get_entrypoint()

@set_interval(1)
def update_ticker():
    if len(webview.windows) > 0:
        webview.windows[0].evaluate_js('window.pywebview.state.setTicker("%d")' % time())


if __name__ == '__main__':
    window = webview.create_window('pywebview-react boilerplate', entry, js_api=Api())
    webview.start(update_ticker, debug=True)

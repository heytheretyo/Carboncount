import json
import os
import subprocess
import threading
import webview
import ctypes
from time import sleep, time
from datetime import datetime
import psutil
import screen_brightness_control as sbc
import time
import gpustat
import multiprocessing
import sys
from PIL import Image
from pystray import Icon, Menu, MenuItem
import os

from file_reader import (
    get_current_emission,
    get_week_emission,
    determine_severity,
    save_statistics,
    load_statistics
)

from calculate_power import (
    calculate_carbon_emmission,
    estimate_power_consumption
)


dir_data = os.path.expanduser("~") + "/.carboncount"
dir_statistics = dir_data + "/statistics.json"
dir_settings = dir_data + "/settings.json"


def get_computer_uptime():
    lib = ctypes.windll.kernel32
    t = lib.GetTickCount64()
    t = int(str(t)[:-3])

    mins, sec = divmod(t, 60)
    hour, mins = divmod(mins, 60)
    days, hour = divmod(hour, 24)

    return [days, hour, mins, sec]


def get_settings():
    default_settings = {
        "DEVICE_TYPE" : "LAPTOP",
        "CPU_POWER" : 50,
        "GPU_POWER" : 90,
        "DISK_POWER" : 8,
        "COUNTRY" : "United Kingdom",
        "ALLOW_NOTIFICATIONS" : False
    }

    if not os.path.exists(dir_settings):
        with open(dir_settings, 'w') as f:
            json.dump(default_settings, f, indent=4)
        return default_settings
    else:
        with open(dir_settings, 'r') as f:
            return json.load(f)


class Api:
    def fullscreen(self):
        webview.windows[0].toggle_fullscreen()


    def save_content(self, content):
        filename = webview.windows[0].create_file_dialog(webview.SAVE_DIALOG)
        if not filename:
            return

        with open(filename, 'w') as f:
            f.write(content)

    def set_settings(self, new_settings):
        settings = {
        "DEVICE_TYPE" : new_settings["type"],
        "CPU_POWER" : new_settings["cpu_power"],
        "GPU_POWER" : new_settings["gpu_power"],
        "DISK_POWER" : 8,
        "COUNTRY" : new_settings["country"],
        "ALLOW_NOTIFICATIONS" : new_settings["allowNotifications"]
        }

        with open(dir_settings, 'w') as f:
            json.dump(settings, f, indent=4)

    def get_settings(self):
        return get_settings()

    def get_data(self):
        today_emmision = get_current_emission()
        week_emmision = get_week_emission()
        severity  = determine_severity(today_emmision)

        data = load_statistics()
        settings = get_settings()
        return {
            "computer_uptime": get_computer_uptime(),
            "carbon_emission": calculate_carbon_emmission(settings),
            "today_emmision": today_emmision,
            "week_emmision": week_emmision,
            "severity": severity,
            "historical_data": data
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


def background_task():
    while True:
        timestamp = datetime.now().date().isoformat()
        power_consumption = estimate_power_consumption(get_settings())
        carbon_emission = calculate_carbon_emmission(get_settings())


        data = {
            "timestamp": timestamp,
            "power_consumption": power_consumption,
            "carbon_emission": carbon_emission
        }

        save_statistics(data, 'timestamp', timestamp)

        sleep(1)

entry = get_entrypoint()

@set_interval(1)
def update_ticker():
    if len(webview.windows) > 0:
        webview.windows[0].evaluate_js('window.pywebview.state.setTicker("%d")' % time())

if __name__ == '__main__':
    window = webview.create_window('carboncount', entry, js_api=Api())

    background_thread = threading.Thread(target=background_task)
    background_thread.daemon = True
    background_thread.start()


    webview.start(update_ticker, debug=True)


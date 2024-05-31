import json
import os
import subprocess
import gpustat
import psutil
import screen_brightness_control as sbc

CPU_IDLE_POWER = 45
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


def estimate_power_consumption(settings):
    cpu_percent = get_cpu_percentage()
    # disk_percent = get_disk_percentage()
    gpu_percent = get_gpu_utilization()

    ram_percent = get_ram_percentage()
    total_ram_power = get_total_ram_power()

    display_brightness = get_display_brightness()

    cpu_power =  (cpu_percent / 100) * settings["CPU_POWER"]
    gpu_power =  (gpu_percent / 100) * settings["GPU_POWER"]
    ram_power = (ram_percent / 100) * total_ram_power
    # disk_power =  (disk_percent / 100) * settings["DISK_POWER"]
    display_power = display_brightness + (display_brightness / 100) * display_brightness

    total_power = cpu_power + gpu_power + ram_power  + display_power
    return total_power



def get_carbon_intensity_data(country):

    try:
        with open(os.getcwd() + "\\src\\data\\carbon_intensity.json", "r") as f:
            data = json.load(f)

        # Filter data for the specified country
        country_data = [entry for entry in data if entry.get("entity") == country]

        if country_data:
            sorted_data = sorted(country_data, key=lambda x: x.get("year"), reverse=True)
            latest_year_data = sorted_data[0]
            return latest_year_data["carbon_intensity"] / 1000
        else:
            return 0.475
    except:
        return 0.475

def calculate_carbon_emmission(settings):
    power_consumption_w = estimate_power_consumption(settings)
    carbon_intensity_kg_co2_per_kwh =  get_carbon_intensity_data(settings["COUNTRY"])

    power_consumption_kwh = power_consumption_w / 1000

    carbon_emissions_kg_co2 = (power_consumption_kwh * carbon_intensity_kg_co2_per_kwh) / 3600

    return carbon_emissions_kg_co2


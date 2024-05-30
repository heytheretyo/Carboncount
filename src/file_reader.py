import os
import json
from datetime import datetime, timedelta
import threading

dir_data = os.path.expanduser("~") + "/.carboncount"
dir_statistics = os.path.join(dir_data, "statistics.json")
lock = threading.Lock()

if not os.path.exists(dir_data):
    os.makedirs(dir_data)


def load_statistics():
    if os.path.exists(dir_statistics):
        with open(dir_statistics, 'r') as f:
            return json.load(f)
    return []

def save_statistics(data, update_key, update_value):
    if os.path.exists(dir_statistics):
        with open(dir_statistics, 'r') as f:
            existing_data = json.load(f)
    else:
        existing_data = []


    with lock:
        if existing_data !=  []:
            no_duplicate = True

            for entry in existing_data:
                if entry.get(update_key) == update_value:

                    newEntry  = {}
                    newEntry["timestamp"] = data["timestamp"]
                    newEntry["power_consumption"] = entry["power_consumption"] + data["power_consumption"]
                    newEntry["carbon_emission"] = entry["carbon_emission"]  + data["carbon_emission"]
                    entry.update(newEntry)

                    no_duplicate = False
                    break

            if no_duplicate:
                existing_data.append(data)
        else:
            existing_data.append(data)


        with open(dir_statistics, 'w') as f:
            json.dump(existing_data, f, indent=4)

def get_current_emission():
    data = load_statistics()
    today = datetime.now().date()

    daily_data = [entry for entry in data if datetime.fromisoformat(entry["timestamp"]).date() == today]
    if not daily_data:
        return 0

    total_power = sum(entry["carbon_emission"] for entry in daily_data)
    return total_power

def get_week_emission():
    data = load_statistics()
    today = datetime.now().date()
    one_week_ago = today - timedelta(days=7)

    weekly_data = [entry for entry in data if one_week_ago <= datetime.fromisoformat(entry["timestamp"]).date() <= today]
    if not weekly_data:
        return 0

    total_power = sum(entry["carbon_emission"] for entry in weekly_data)
    return total_power



def determine_severity(average_power):
    if average_power < 100:
        return "Low"
    elif average_power < 200:
        return "Moderate"
    else:
        return "High"


def fetch_weekly_data():
    data = load_statistics()

    today = datetime.now().date()
    start_of_week = today - timedelta(days=today.weekday())  # Monday of the current week
    end_of_week = start_of_week + timedelta(days=6)  # Sunday of the current week

    daily_data = [{"day": (start_of_week + timedelta(days=i)).strftime("%A"), "total_power_consumption": 0, "total_carbon_emission": 0, "num_entries": 0}
                  for i in range(7)]

    for entry in data:
        entry_date = datetime.fromisoformat(entry["timestamp"]).date()
        if start_of_week <= entry_date <= end_of_week:
            day_index = (entry_date - start_of_week).days
            daily_data[day_index]["total_power_consumption"] += entry["power_consumption"]
            daily_data[day_index]["total_carbon_emission"] += entry["carbon_emission"]
            daily_data[day_index]["num_entries"] += 1

    return daily_data

def fetch_monthly_data():
    data = load_statistics()
    current_year = datetime.now().year
    monthly_data = [{"month": month, "total_power_consumption": 0, "total_carbon_emission": 0, "num_entries": 0}
                    for month in range(1, 13)]

    for entry in data:
        entry_date = datetime.fromisoformat(entry["timestamp"]).date()
        if entry_date.year == current_year:
            month = entry_date.month
            monthly_data[month - 1]["total_power_consumption"] += entry["power_consumption"]
            monthly_data[month - 1]["total_carbon_emission"] += entry["carbon_emission"]
            monthly_data[month - 1]["num_entries"] += 1

    return monthly_data
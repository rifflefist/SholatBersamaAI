import configparser
import os
from datetime import datetime
from assets.helper.get_resource import resource_path

def save_settings(camera, orientation, time):
    config = configparser.ConfigParser()
    
    config["Settings"] = {
        "camera": str(camera),
        "orientation": str(orientation),
        "time": time,
        "time_saved": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    filename = resource_path("assets/settings.ini")

    with open(filename, "w") as configfile:
        config.write(configfile)

def load_settings():
    
    filename = resource_path("assets/settings.ini")
    
    config = configparser.ConfigParser()

    if not os.path.exists(filename):
        return {
            "camera": 0,
            "orientation": 0,
            "time": datetime.now().strftime("%H:%M")
        }

    config.read(filename)

    settings = config["Settings"]
    
    time_dynamic = hitung_waktu_baru(settings.get("time"), settings.get("time_saved"))
    
    return {
        "camera": int(settings.get("camera", 0)),
        "orientation": int(settings.get("orientation", 0)),
        "time": time_dynamic
    }

def hitung_waktu_baru(time_settings_str, time_saved_str):

    time_now = datetime.now()
    time_saved = datetime.strptime(time_saved_str, "%Y-%m-%d %H:%M:%S")

    diff = time_now - time_saved

    today = datetime.now().date()
    time_settings = datetime.strptime(time_settings_str, "%H:%M")
    time_settings = datetime.combine(today, time_settings.time())

    time_real = time_settings + diff

    return time_real.strftime("%H:%M")
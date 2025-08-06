from datetime import datetime

def get_time():
    now = datetime.now()
    return now.strftime("%H"), now.strftime("%M")

def get_salat_time(time):
    salat_wajib = ["Shubuh", "Dzuhur", "Ashar", "Maghrib", "Isya"]
    waktu_salat = ["04:52", "06:15", "12:27", "15:51", "15:51", "18:36", "18:36", "19:50", "19:50", "04:52"]
    
    format_time = "%H:%M"
    
    if datetime.strptime(time, format_time) >= datetime.strptime(waktu_salat[0], format_time) and datetime.strptime(time, format_time) <= datetime.strptime(waktu_salat[1], format_time):
        return salat_wajib[0]
    elif datetime.strptime(time, format_time) >= datetime.strptime(waktu_salat[2], format_time) and datetime.strptime(time, format_time) <= datetime.strptime(waktu_salat[3], format_time):
        return salat_wajib[1]
    elif datetime.strptime(time, format_time) >= datetime.strptime(waktu_salat[4], format_time) and datetime.strptime(time, format_time) <= datetime.strptime(waktu_salat[5], format_time):
        return salat_wajib[2]
    elif datetime.strptime(time, format_time) >= datetime.strptime(waktu_salat[6], format_time) and datetime.strptime(time, format_time) <= datetime.strptime(waktu_salat[7], format_time):
        return salat_wajib[3]
    elif datetime.strptime(time, format_time) >= datetime.strptime(waktu_salat[8], format_time) or datetime.strptime(time, format_time) <= datetime.strptime(waktu_salat[9], format_time):
        return salat_wajib[4]
    else:
        return "Tidak Waktunya"
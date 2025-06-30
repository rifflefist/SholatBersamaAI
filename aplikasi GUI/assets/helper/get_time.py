from datetime import datetime

def get_time():
    now = datetime.now()
    return now.strftime("%H"), now.strftime("%M")
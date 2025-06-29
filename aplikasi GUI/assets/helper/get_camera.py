import subprocess
import re
from assets.helper.get_resource import resource_path

def get_camera():
    
    ffmpeg_path = resource_path("assets/helper/ffmpeg.exe")
    
    try:
        result = subprocess.run(
            [ffmpeg_path, "-list_devices", "true", "-f", "dshow", "-i", "dummy"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True  # penting: agar hasilnya berupa string, bukan bytes
        )
        output = result.stderr  # karena ffmpeg tulis ke stderr
    except FileNotFoundError:
        print("FFmpeg tidak ditemukan.")
        return []
    
    # Filter hanya nama kamera
    pattern = r'"(.+?)"\s*\(video\)'
    kamera_ditemukan = re.findall(pattern, output)
    return kamera_ditemukan

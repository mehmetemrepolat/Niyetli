from MediaControl import WindowsOsControl
import os
import psutil


battery = psutil.sensors_battery()
percent = battery.percent

print(f"Şarj seviyesi: {percent}%")

#os.system("shutdown /a")
#os = windows_os_control()

#os.set_brigthness(100)
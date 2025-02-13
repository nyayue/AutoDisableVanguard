import psutil
import subprocess
import winreg 
import os
import sys

# the path (duh)
REGISTRY_PATH = r"Software\AutoDisableVanguard"

# as what to save the key
REGISTRY_RunVanguard = "RunVanguard"

# path for autostart folder
AUTOSTART_PATHS = [
    os.path.expandvars(r"%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"),  # user autostart
    os.path.expandvars(r"%ProgramData%\Microsoft\Windows\Start Menu\Programs\Startup")  # global autostart
]

def register_value(name, value): # add value to registry
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, REGISTRY_PATH, 0, winreg.KEY_SET_VALUE) as key:
            winreg.SetValueEx(key, name, 0, winreg.REG_DWORD, int(value))
    except FileNotFoundError:
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, REGISTRY_PATH) as key:
            winreg.SetValueEx(key, name, 0, winreg.REG_DWORD, int(value))

def read_value(name): # read value from registry
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, REGISTRY_PATH, 0, winreg.KEY_READ) as key:
            value, _ = winreg.QueryValueEx(key, name)
            return value
    except FileNotFoundError:
        return 0 # default value
        
def kill_task(): # kill task
    for proc in psutil.process_iter(['pid', 'name']):
        if "vgtray.exe" in proc.info['name'].lower():
            try:
                proc.terminate()
                subprocess.run("sc stop vgc", shell=True)
                subprocess.run("sc stop vgk", shell=True)
            except psutil.NoSuchProcess:
                pass
            
def run():
    if os.path.dirname(os.path.abspath(sys.argv[0])) in AUTOSTART_PATHS:
        if read_value(REGISTRY_RunVanguard) == 0: # if 0, process it gets stopped, else wont get stopped
            kill_task()
        else:
            register_value(REGISTRY_RunVanguard, 0)

if __name__ == "__main__":
    run()
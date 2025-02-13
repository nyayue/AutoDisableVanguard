import subprocess   
import tkinter as tk
from tkinter import messagebox
import winreg

# the path (duh)
REGISTRY_PATH = r"Software\AutoDisableVanguard"

# as what to save the key
REGISTRY_RunVanguard = "RunVanguard"

def register_value(name, value): # add value to registry
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, REGISTRY_PATH, 0, winreg.KEY_SET_VALUE) as key:
            winreg.SetValueEx(key, name, 0, winreg.REG_DWORD, int(value))
    except FileNotFoundError:
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, REGISTRY_PATH) as key:
            winreg.SetValueEx(key, name, 0, winreg.REG_DWORD, int(value))

def restart(): # restarts pc
     subprocess.run(["shutdown", "/r", "/t", "0"])

def question(): # ask if the pc should get restarted and run vanguard?
    root = tk.Tk()
    root.withdraw()
    
    antwort = messagebox.askquestion("Confirm restart", "Would you like to restart the pc and run vanguard?", icon='question')

    if antwort == 'yes':
        register_value(REGISTRY_RunVanguard, 1)
        restart()

if __name__ == "__main__":
    question
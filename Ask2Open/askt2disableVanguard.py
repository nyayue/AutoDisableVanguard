import psutil
import subprocess   
import tkinter as tk
from tkinter import messagebox
import winreg 
import os
        
def kill_task(): # kill task
    for proc in psutil.process_iter(['pid', 'name']):
        if "vgtray.exe" in proc.info['name'].lower():
            try:
                proc.terminate()
                subprocess.run("sc stop vgc", shell=True)
                subprocess.run("sc stop vgk", shell=True)
            except psutil.NoSuchProcess:
                pass

def restart(): # restarts pc
     subprocess.run(["shutdown", "/r", "/t", "0"])

def question(): # ask if the pc should get restarted and run vanguard?
    root = tk.Tk()
    root.withdraw()
    
    antwort = messagebox.askquestion("Stop Vanguard?", "Would you like to stop vanguard from running?", icon='question')

    if antwort == 'yes':
        kill_task()

if __name__ == "__main__":
    question()
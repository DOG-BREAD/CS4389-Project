import tkinter as tk
from tkinter import ttk, simpledialog
import ipaddress
import subprocess
import threading
import netifaces 

# endthread=False
def destroy(x):
    x.destroy()
    return

def runPortScan(path, ip_address):
    portScan = subprocess.run(['python', path, str(ip_address)])
    
def scan_ip(ip_address):

    progress_window = tk.Toplevel(root)
    progress_window.title("Scanning Progress")
    progress_window.geometry("300x150")
    
    progress_label = tk.Label(progress_window, text=f"Scanning {ip_address}...", font=("Helvetica", 20))
    progress_label.pack(pady=10)
    progress_bar = ttk.Progressbar(progress_window, orient='horizontal', mode='indeterminate', length=100)
    progress_bar.pack()
    progress_bar.start(3)
    
    #start the port scanner thread 
    thread2 = threading.Thread(target=runPortScan, args=['portScanner/PortScanner.py',ip_address])
    thread2.start()
    
    #destroy after 40 seconds , call destroy method, pass the window
    progress_window.after(40000,destroy,progress_window)
    root.mainloop()


def scan_port():
    ip_address = simpledialog.askstring("Enter IP Address", "Please enter the IP address:")
    
    if ip_address is not None:
        try:
            ipaddress.ip_address(ip_address)
            
            thread = threading.Thread(target=scan_ip, args=[ip_address],daemon=True)
            thread.start()
            
            # scan_ip(ip_address)
                
            
            # endthread=True
            
        except ValueError:
            error_label = tk.Label(simpledialog._dialog_window, text="Invalid IP address format. Please try again.", fg="red")
            error_label.pack(pady=5)

def analyze():
    analyz = subprocess.run(['python', 'Analyzer/main.py'],shell=True)

def analyzeWindow():
    progress_window = tk.Toplevel(root)
    progress_window.title("Analyze")
    progress_window.geometry("400x250")
    
    progress_label = tk.Label(progress_window, text=f"Analyzing", font=("Helvetica", 20))
    progress_label.pack(pady=10)
    progress_bar = ttk.Progressbar(progress_window, orient='horizontal', mode='indeterminate', length=100)
    progress_bar.pack()
    progress_bar.start(3)

    thread = threading.Thread(target=analyze,daemon=True)
    thread.start()



    root.mainloop()
    
def attack_target():
    pass

root = tk.Tk()
root.title("Port Scanner")
root.geometry("600x400")

background_image = tk.PhotoImage(file="gui/hack.png")
background_label = tk.Label(root, image=background_image)
background_label.place(relwidth=1, relheight=1)

title_label = tk.Label(root, text="PORT SCANNER", font=("Helvetica", 36, "bold"), highlightbackground="black", highlightthickness=5)
title_label.pack(pady=(40, 20))

button_font = ("Helvetica", 24,'bold', 'underline')



scan_button = tk.Button(root, text="Scan", command=scan_port, font=button_font,foreground="black", width=20)
attack_button = tk.Button(root, text="Analyze", command=analyzeWindow, font=button_font,foreground="black", width=20)
exit_button = tk.Button(root, text="Exit", command=root.quit, font=button_font,foreground="black", width=20)

scan_button.pack(pady=10)
attack_button.pack(pady=10)
exit_button.pack(pady=10)


root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)


root.mainloop()

import tkinter as tk
from tkinter import ttk, simpledialog
import ipaddress

def scan_ip(ip_address):
    progress_window = tk.Toplevel(root)
    progress_window.title("Scanning Progress")
    progress_window.geometry("300x150")
    
    progress_label = tk.Label(progress_window, text=f"Scanning {ip_address}...", font=("Helvetica", 20))
    progress_label.pack(pady=10)
    progress_bar = ttk.Progressbar(progress_window, orient='horizontal', mode='indeterminate', length=100)
    progress_bar.pack()
    progress_bar.start(3)
    

def scan_port():
    ip_address = simpledialog.askstring("Enter IP Address", "Please enter the IP address:")
    
    if ip_address is not None:
        try:
            ipaddress.ip_address(ip_address)
            scan_ip(ip_address)
        except ValueError:
            error_label = tk.Label(simpledialog._dialog_window, text="Invalid IP address format. Please try again.", fg="red")
            error_label.pack(pady=5)

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
attack_button = tk.Button(root, text="Attack", command=attack_target, font=button_font,foreground="black", width=20)
exit_button = tk.Button(root, text="Exit", command=root.quit, font=button_font,foreground="black", width=20)

scan_button.pack(pady=10)
attack_button.pack(pady=10)
exit_button.pack(pady=10)


root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

root.mainloop()

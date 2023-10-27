import tkinter as tk
from tkinter import ttk, simpledialog
import ipaddress
import subprocess
import threading
import netifaces 
from tksheet import Sheet
from Analyzer.main import *

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
 
        except ValueError:
            error_label = tk.Label(simpledialog._dialog_window, text="Invalid IP address format. Please try again.", fg="red")
            error_label.pack(pady=5)

interface_option = None
def getInterface():
    interfaces = get_net_interface()
    interfaces = interfaces.values()
    if interface_option is None:
        dialog = tk.Toplevel(root)
        def save_option(option):
            global interface_option
            dialog.destroy()
            interface_option = option
            analyzeWindow()

        # Create a button for each network interface
        for interface in interfaces:
            button = tk.Button(dialog, text=interface, command=lambda i=interface: save_option(i))
            button.pack()
        # print(interface_option)
        
    if interface_option is not None:
        print(interface_option)
        analyzeWindow()


def populate_treeview(data_frame, tree):
    # Clear the existing items in the Treeview
    for i in tree.get_children():
        tree.delete(i)

    # Insert the columns from the DataFrame
    tree["columns"] = list(data_frame.columns)
    tree.heading("#0", text="Index")  # Special column for index
    for column in data_frame.columns:
        tree.heading(column, text=column)
        # tree.column(column, anchor='center')
        tree.column(column, width=100)  # Adjust the width as needed

    # Insert the data into the Treeview
    for index, row in data_frame.iterrows():
        tree.insert("", "end", text=index, values=list(row))

def start_scan_analysis(tree):
    driver(interface_option)
    threat_list = get_threat_list()
    populate_treeview(threat_list, tree)
    return
    

def analyzeWindow():
    print(f"IN analyzeWindow: interface_option ====== {interface_option}")
    progress_window = tk.Toplevel(root)
    progress_window.title("Analyzer")
    progress_window.geometry("1400x750")

    test_label_var = tk.StringVar()
    test_label_var.set(f"Port Scanning Analysis: [{interface_option}]")
    
    test_label = tk.Label(progress_window, textvariable=test_label_var)
    test_label.pack()
    
    # create a button to start the test
    start_test_button = tk.Button(progress_window, text="Start Test", command=lambda: start_scan_analysis(tree))
    start_test_button.pack(pady=10)

    tree = ttk.Treeview(progress_window)
    ttk.Style().configure("Treeview", font=('Helvetica', 12))
    
    tree.config(height=15, show='headings')
    tree.pack(fill='both', expand=True)

    data_frame = get_threat_list()
    populate_treeview(data_frame, tree)

    progress_window.mainloop()
    
    
def attack_target():
    pass

def main():
    global root
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
    analysis_button = tk.Button(root, text="Analyze", command=getInterface, font=button_font,foreground="black", width=20)
    exit_button = tk.Button(root, text="Exit", command=exit, font=button_font,foreground="black", width=20)

    scan_button.pack(pady=10)
    analysis_button.pack(pady=10)
    exit_button.pack(pady=10)

    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    root.mainloop()

if __name__ == "__main__":
    main()
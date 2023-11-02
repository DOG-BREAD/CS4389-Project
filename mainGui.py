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

hasbooted = False
interface_option = None
def getInterface():
    interfaces = get_net_interface()
    interfaces = interfaces.items()

    if interface_option is None:
        dialog = tk.Toplevel(root)
        dialog.title("Select A Network Interface")
        def save_option(option):
            global interface_option
            dialog.destroy()
            interface_option = option
            if hasbooted:
                # change the label to reflect the new interface
                test_label_var.set(f"Port Scanning Analysis: Interface: {interface_option[0]}, IP: {interface_option[1]}")
                clear_threat_list()
                return
            else:
                clear_threat_list()
                analyzeWindow(interface_option)
                interface_option = None
                root.mainloop()
                
        # Create a button for each network interface
        for interface in interfaces:
            button = tk.Button(dialog, text=f"{interface[0]} : {interface[1]}", height=5, width=60, command=lambda i=interface: save_option(i))
            button.pack()
    root.mainloop()


def populate_treeview(data_frame, tree):
    # Clear the existing items in the Treeview
    for i in tree.get_children():
        tree.delete(i)

    # Insert the columns from the DataFrame
    tree["columns"] = list(data_frame.columns)
    tree.heading("#0", text="Index")  # Special column for index
    for column in data_frame.columns:
        tree.heading(column, text=column)
        tree.column(column, width=100)  # Adjust the width as needed

    # Insert the data into the Treeview
    for index, row in data_frame.iterrows():
        tree.insert("", "end", text=index, values=list(row))

def start_scan_analysis(tree, interface_option, root):
    clear_threat_list()
    driver(interface_option)
    threat_list = get_threat_list()
    if len(threat_list) > 0:
        print(f"TESTING {threat_list}")
    else:
        print("No threats found")
        display_no_threats_found(root)
    populate_treeview(threat_list, tree)

def clear_interface(tree, progress_window):
    global interface_option
    interface_option = None
    progress_window.destroy()
    clear_threat_list()
    getInterface()
    populate_treeview(get_threat_list(), tree)


def display_no_threats_found(root):
    no_threats_window = tk.Toplevel(root)
    no_threats_window.title("No Port Scanning Detected")
    no_threats_window.geometry("350x100")

    no_threats_label = tk.Label(no_threats_window, text="No Threats Detected!", font=("Helvetica", 25))
    no_threats_label.pack(pady=10)

    ok_button = tk.Button(no_threats_window, text="OK", command=lambda: no_threats_window.destroy())
    ok_button.pack(pady=5)

    root.mainloop()


def analyzeWindow(interface_option: list):
    progress_window = tk.Toplevel(root)
    progress_window.title("Analyzer")
    progress_window.attributes('-fullscreen', True)
    progress_window.configure(bg='#e87500')
    global hasbooted
    hasbooted = True

    global test_label_var
    test_label_var = tk.StringVar()
    test_label_var.set(f"Port Scanning Analysis: Interface: {interface_option[0]}, IP: {interface_option[1]}")

    
    test_label = tk.Label(progress_window, textvariable=test_label_var)
    test_label.pack()
    
    # create a button to start the test
    start_test_button = tk.Button(progress_window, text="Start Detection & Analysis", command=lambda: start_scan_analysis(tree, interface_option, root))
    start_test_button.pack(padx=5, pady=2)
    
    clear_interface_button = tk.Button(progress_window, text="Clear Results & Change Interface", command=lambda: clear_interface(tree, progress_window))
    clear_interface_button.pack(padx=5, pady=2)
    
    tree = ttk.Treeview(progress_window)
    ttk.Style().configure("Treeview", font=('Helvetica', 12),background ="#154734", fieldbackground="#154734",foreground="white"  )
    
    tree.config(height=15, show='headings')
    tree.pack(fill='both', expand=True)

    data_frame = get_threat_list()
    populate_treeview(data_frame, tree)
    hasbooted = False
    
def main():
    global root
    root = tk.Tk()
    root.title("Port Scanner")
    # root.geometry("600x400")

    window_width = 600
    window_height = 400

    # my commit message should be ASS


    # Get the screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")


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

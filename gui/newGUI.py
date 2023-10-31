from tkinter import *
from tkinter import ttk
import threading
from main import driver, get_net_interface, get_threat_list
from main import analyze_ip



def main():
    global root
    root = Tk()
    root.title('Port Scanner')

    # Adjust size of the window
    root.geometry("800x600")
    
    #load background pic
    background_image = PhotoImage(file="tron_tunnels.png")

    #Use a modern theme
    style = ttk.Style()
    style.theme_use("alt")
    
    #creat a label with background image
    background_label = Label(root, image=background_image)
    background_label.place(relwidth=1, relheight=1)

    #Set background color using the style
    style.configure("TFrame", background="#282c34")
    style.configure("TButton", padding=10, background="purple", foreground="red")

    # Icon for the window
    root.iconphoto(True, PhotoImage(file="guy.png"))
    
    # Buttons
    exit_button = ttk.Button(root, text="Exit", command=root.quit, style="TButton")
    exit_button.place(relx=0.5, rely=0.2, anchor=CENTER)

    scan_button = ttk.Button(root, text="Scan Ports", command=scanCallBack, style="TButton")
    scan_button.place(relx=0.5, rely=0.4, anchor=CENTER)
    
    analyze_button = ttk.Button(root, text="Analyze IP", command=analyzeCallBack, style="TButton")
    analyze_button.place(relx=0.5, rely=0.8, anchor=CENTER)

    attack_button = ttk.Button(root, text="Attack!", command=attackCallBack, style="TButton")
    attack_button.place(relx=0.5, rely=0.6, anchor=CENTER)

    root.mainloop()

def scanCallBack():
    global message
    message = Toplevel(root)  # makes a pop up in front of other windows at root level
    message.title("Scanning")
    message.geometry("700x400")
    message.config(bg="#282c34")  # Use the same background color as in the main function
    
    #background_image
    background_image = PhotoImage(file="2nd.png")

    message_label = Label(message, text="Scanning", bg='#282c34', fg='white') 
    message_label.pack(pady=10)

    message_frame = Frame(message, bg="#282c34")  # Use the same background color as in the main function
    message_frame.pack(pady=10)

    # progress bar needed below
    pb = ttk.Progressbar(message, orient='horizontal', mode='indeterminate', length=250)
    pb.pack()
    pb.start(7)

    # frame for displaying scan data
    scan_data_frame = Frame(message_frame, bg="#282c34")
    scan_data_frame.pack(pady=10)
    
    # placeholder label for scan data
    scan_data_label = Label(scan_data_frame, text="Scan Data Goes Here", bg="#282c34", fg="white")
    scan_data_label.pack()

    stop_scanning = ttk.Button(message, text="Exit", command=message.destroy, style="TButton")
    stop_scanning.pack(pady=10)
    
    # Call the port scanning function from the backend script
    # You might need to adjust the arguments based on your needs
    driver_thread = threading.Thread(target=driver, args=(get_net_interface(),))
    driver_thread.start()
    # Wait for the thread to finish before displaying results
    driver_thread.join()

    # Update the label with scan data
    scan_data_label.config(text=f"Scan Data:\n{get_threat_list()}")
    
    
def analyzeCallBack():
    global message
    message = Toplevel(root)
    message.title("Analyze IP")
    message.geometry("400x200")
    message.config(bg="#282c34")

    message_label = Label(message, text="Enter IP to analyze:", bg='#282c34', fg='white')
    message_label.pack(pady=10)

    ip_entry = Entry(message)
    ip_entry.pack(pady=10)

    analyze_button = ttk.Button(message, text="Analyze", command=lambda: analyze_ip(ip_entry.get()))
    analyze_button.pack(pady=10)
    
		


def yesAttack():
    print("hi")
    

def attackCallBack():
    global message
    message = Toplevel(root)
    message.title("sus attack")
    message.geometry("700x500")
    message.config(bg="#282c34")

    #global attack_Image
    attack_Image = PhotoImage(file="2nd.png")

    message_label = Label(message, text="would you like to counter attack?", bg='#282c34', fg='white')
    message_label.pack(pady=10)

    message_frame = Frame(message)
    message_frame.pack(pady=10)
     
    image = Label(message_frame, image=attack_Image)
    image.pack()

    Yes_button = Button(message, text="Yes!", command=yesAttack)
    Yes_button.place(relx=0.5, rely=0.2, anchor=CENTER, width=50, height=30)
    No_button = Button(message, text="No!", command=message.destroy)
    No_button.place(relx=0.5, rely=0.5, anchor=CENTER, width=50, height=30)

    

if __name__ == "__main__":
    main()

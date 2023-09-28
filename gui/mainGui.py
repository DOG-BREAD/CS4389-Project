from tkinter import *
from tkinter import ttk

def main():
    root = Tk()
    root.title('Port Scanner')

    # Adjust size of the window
    root.geometry("800x800")
    root.configure(bg="#E63946")

    #style for buttons
    # style=Style()
    # style.configure()

    exit_button = Button(root, text="Exit", command=root.quit)
    exit_button.place(relx=0.01, rely =0.01, anchor=NW)
    scan_button = Button(root, text="Scan Ports")
    scan_button.place(relx =0.01, rely=0.05, anchor=NW)

    # need to add progress bar once scan is clicked
    # 

    root.mainloop()

if __name__=="__main__":
    main()
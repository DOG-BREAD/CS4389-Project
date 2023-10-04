from tkinter import *
from tkinter import ttk
import time

def main():
    root = Tk()
    root.title('Port Scanner')

    # Adjust size of the window
    root.geometry("800x600")
    root.configure(bg="#E63946")

    #style for buttons
    # style=Style()
    # style.configure()

    #scanning 
    def scanCallBack():
        global message
        message = Toplevel(root) # makes a pop up infront of other windows at root level
        message.title("Scanning")
        message.geometry("400x300")
        message.config(bg="black")

        
        message_label = Label(message, text = "Scanning", bg='white')
        message_label.pack(pady = 10)

        message_frame = Frame(message)
        message_frame.pack(pady=5)
        #progress bar needed below 

        pb = ttk.Progressbar(message, orient='horizontal',mode='indeterminate',length=100)
        pb.pack()
        pb.start(3)

        stopScanning = Button(message, text="exit",command = message.destroy)
        stopScanning.pack()

        
        #needs frame inside to display scan data 

#############################################################################################################
   
   
    #Attack sensed , pop up window for interaction
    def yesAttack():
            print("hi")


        #attack function for Yes_button
    def attackCallBack():
        global message
        message = Toplevel(root) # makes a pop up infront of other windows at root level
        message.title("sus attack")
        message.geometry("1920x1080")
        message.config(bg="black")

        global attack_Image # needs global to be accessed outside of def
        attack_Image = PhotoImage(file= "gui/guy.png")

        message_label = Label(message, text = "would you like to counter attack?", bg='white')
        message_label.pack(pady = 10)

        message_frame = Frame(message)
        message_frame.pack(pady=5)

        image = Label(message_frame, image=attack_Image )
        image.pack()
        
        Yes_button = Button(message, text="Yes!",command = yesAttack )
        Yes_button.place(relx =0.01, rely=0.1, anchor=NW, width=30, height= 30)
        No_button = Button(message, text="No!",command = message.destroy)
        No_button.place(relx =0.01, rely=0.5, anchor=NW , width=30, height= 30)
        #needs to launch attack and show whats done , close window and go back to main skeleton frame
        

 
###################################################################################################################3
    exit_button = Button(root, text="Exit", command=root.quit)
    exit_button.place(relx=0.01, rely =0.01, anchor=NW)
    scan_button = Button(root, text="Scan Ports", command = scanCallBack)
    scan_button.place(relx =0.01, rely=0.05, anchor=NW)
    attack_button = Button(root, text="Attack!",command = attackCallBack )
    attack_button.place(relx =0.01, rely=0.1, anchor=NW)

    root.mainloop()

if __name__=="__main__":
    main()
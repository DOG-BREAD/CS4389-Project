import sys
import socket
import ipaddress
from datetime import datetime
import threading
import concurrent.futures

class PortScanner:
    def __init__(self, min=1, max=65535, target="127.0.0.1"):
        self.min = min
        self.max = max
        self.target = target

    def scan_port(self):
        def validate_ip_address(ip_string):
            try:
                ip_object = ipaddress.ip_address(ip_string)
                print("The IP address '{ip_object}' is valid.")
                return True
            except ValueError:
                print("The IP address '{ip_string}' is not valid")
                return False

        startup = 'Starting port scanner...'
        print(startup)

        # Add Banner
        print("-" * 50)
        print("Scanning Target: " + target)
        print("Scanning started at:" + str(datetime.now()))
        print("-" * 50)

        listPorts = []
        try:
            if validate_ip_address(target) == True:
                # scan between set min and max, auto set to 1-65535
                for port in range(self.min, self.max):
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    socket.setdefaulttimeout(1)

                    # returns an error indicator
                    result = s.connect_ex((target, port))
                    if result == 0:
                        print("Port {} is open".format(port))
                        listPorts.append(port)
                    s.close()
            else:
                sys.exit()
        except socket.gaierror:
            print("\n Hostname Could Not Be Resolved")
            sys.exit()
        except socket.error:
            print("\n Server not responding")
            sys.exit()
        return listPorts


if __name__ == "__main__":
    target = input("Enter target address: ")

    # converting to threads
    threadarray = []
    for x in range(0, 65000, 1000):
        test = PortScanner(x, x+999, target)
        thread = threading.Thread(target=test.scan_port)
        threadarray.append(thread)
        print(f"I am starting {x}")
        thread.start()

    #for last portion 
    for x in range(65000, 65535,535):
        test = PortScanner(x, x+535, target)
        thread = threading.Thread(target=test.scan_port)
        threadarray.append(thread)
        print(f"I am starting {x}")
        thread.start()

    listOfPorts=[]
    #join the threads
    for x in threadarray:
        # listOfPorts.append(x)
        # print(x)
        x.join()

    print(listOfPorts)
    

import sys
import socket
from datetime import datetime

class PortScanner: 
    def _init_(self, min = 1, max = 65535):
        self.min = min
        self.max = max
    
    def scan_port(self, target):
        startup = 'Starting port scanner...'
        print(startup)

        # Add Banner 
        print("-" * 50)
        print("Scanning Target: " + target)
        print("Scanning started at:" + str(datetime.now()))
        print("-" * 50)
        
        listPorts = []
        try:
            # will scan ports between 1 to 65,535
            for port in range(self.min, self.max):
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                socket.setdefaulttimeout(1)
                
                # returns an error indicator
                result = s.connect_ex((target,port))
                if result ==0:
                    print("Port {} is open".format(port))
                    listPorts.append(port)
                s.close()
        
        except socket.gaierror:
                print("\n Hostname Could Not Be Resolved")
                sys.exit()
        except socket.error:
                print("\n Server not responding")
                sys.exit()
        return listPorts
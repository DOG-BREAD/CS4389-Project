import sys
import socket, threading
import ipaddress
from datetime import datetime

class PortScanner: 
    def __init__(self, min = 1, max = 65535):
        self.min = min
        self.max = max

    def scan_ports(self, target):

        # Add Banner

        startup = 'Starting port scanner...'
        print(startup)
        print("-" * 50)
        print("Scanning Target: " + target)
        print("Scanning started at:" + str(datetime.now()))
        print("-" * 50)

        open_ports = []
        threds = []
        try:
            if self.validate_ip_address(target) == True:
                self.create_threads(target, open_ports,threds)
                self.start_threads(threds)
                self.join_threads(threds)
            else:
                sys.exit()
        except socket.gaierror:
            print("\n Hostname Could Not Be Resolved")
            sys.exit()
        except socket.error:
            print("\n Server not responding")
            sys.exit()
        self.write_file(open_ports)
        return open_ports
    
    def validate_ip_address(self,ip_string):
        try:
            ip_object = ipaddress.ip_address(ip_string)
            print("The IP address '{}' is valid.".format(ip_object))
            return True
        except ValueError:
            print("The IP address '{}' is not valid".format(ip_string))
            return False
        
    def check_port (self, target, port, open_ports):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(1)
        result = s.connect_ex((target,port))
        if result ==0:
            print("Port {} is open".format(port))
            open_ports.append(port)
        s.close()
        
    def create_threads(self, target, open_ports, threds):
        for port in range(self.min, self.max):
            thread = threading.Thread(target=self.check_port, args=(target,port, open_ports))
            threds.append(thread)

    def start_threads(self,threds):
        for i in range(self.min-1, self.max-1):
            threds[i].start()

    def join_threads(self,threds):
        for i in range(self.min-1, self.max-1):
            threds[i].join()

    def write_file(self, open_ports):
        file = open('ports.txt', 'w')
        for port in open_ports:
            file.write(str(port))
            file.write('\n')
        file.close()
        return


if __name__ == "__main__":
    # print("Enter target a")
    target = sys.argv[1]
    print(str(target))
    test = PortScanner()
    test.scan_ports(target)
    print("Finished Scanning For Open Ports")
    exit(0)
    

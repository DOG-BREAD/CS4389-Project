import sys
import socket
import ipaddress
from datetime import datetime


class PortScanner:
    def __init__(self, min=1, max=65535):
        self.min = min
        self.max = max

    def scan_port(self, target):
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
    test = PortScanner()

    test.scan_port(target)

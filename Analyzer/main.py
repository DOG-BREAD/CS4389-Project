import pyshark
import socket
import netifaces as ni
from scapy.all import IFACES
import pandas as pd

SCAN_FILE = './scan_result.pcap'

class InvalidChoice(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return f"Cannot find host: '{self.message}'"

class Analyze:
    def __init__(self):
        self.interface = self.get_net_interface()

    # Method within Analyze to choose which network interface on a device to listen to.
    # Made for devices with multiple interfaces (i.e. has VM network adapters)
    # Returns a tuple of the format ('Interface Name', 'Interface IP')
    def get_net_interface(self):
        ifdict=IFACES.data
        ifaces = ni.interfaces()
        select = []
    
        print('Active interfaces:')
        for iface in ifaces:
            try:
                ip = ni.ifaddresses(iface)[ni.AF_INET][0]["addr"]
                print(f"IP: {ip} from Interface: {ifdict[iface].name} {iface}")
                select.append((ifdict[iface].name, ip))
            except:
                pass
        # enumerate the select list and convert to a dictionary        
        select = dict(enumerate(select))
        
        while True:
            print('\nChoose your interface to analyze by index below:')
            for x in select:
                print(f'{x} : {select[x][0]}')
            try:
                ifchoice = int(input('Choose an interface index value: '))
                if ifchoice in select.keys():
                    break
                else:
                    raise InvalidChoice('Invalid choice for interface select.')
            except InvalidChoice:
                print(f"'{ifchoice}' is not a valid index on the interface list.\n")
            except ValueError:
                print('Please input numeric value only.\n')
        
        print(f"Chosen interface is '{select[ifchoice][0]}' with IP: {select[ifchoice][1]}")
        return select[ifchoice]

    def tcp_scan(self, read_file):
        print(f"getting TCP traffic data on interface {self.interface[0]} (IP: {self.interface[1]})")

        dst = f'ip.dst=={self.interface[1]} && tcp'
        print(dst)
        tcp_cap = pyshark.FileCapture(input_file=read_file, display_filter=dst)

        data = []

        for packet in tcp_cap:
            data.append({
                'source': packet.ip.src,
                'src-port': packet.tcp.srcport,
                'destination': packet.ip.dst,
                'dst-port': packet.tcp.dstport,
                'protocol': packet.transport_layer,
                'length': packet.length,
                'time': packet.sniff_time,
            })

        df = pd.DataFrame(data)
        print(df.head())
        # print(df.groupby(['source']))
        f = open('panda_write_tcp.txt', 'a')
        f.write(df.to_string())
        f.close()


    def udp_scan(self, read_file):
        print(f"getting UDP traffic data on interface {self.interface[0]} (IP: {self.interface[1]})")
        dst = f'ip.dst=={self.interface[1]} && udp'
        print(dst)
        udp_cap = pyshark.FileCapture(input_file=read_file, display_filter=dst)
        
        data = []

        for packet in udp_cap:
            data.append({
                'source': packet.ip.src,
                'src-port': packet.udp.srcport,
                'destination': packet.ip.dst,
                'dst-port': packet.udp.dstport,
                'protocol': packet.transport_layer,
                'length': packet.length,
                'time': packet.sniff_time,             
            })

        df = pd.DataFrame(data)
        print(df.head())
        # print(df.groupby(['source']))
        
        f = open('panda_write_udp.txt', 'a')
        f.write(df.to_string())
        f.close()


class main:

    a1 = Analyze()

    while True:
        try:
            sniff_length = int(input("How long (seconds) do you want to capture? "))
        except ValueError:
            print('Please input numeric value only.\n')
        else:
            break

    print(f"sniffing for {sniff_length} packets")
    live = pyshark.LiveCapture(interface= a1.interface[0],output_file=SCAN_FILE).sniff(timeout=sniff_length)
    print("done sniffing")
    
    a1.tcp_scan(SCAN_FILE)
    # a1.udp_scan(SCAN_FILE)
    

if __name__=="__main__":
    main()
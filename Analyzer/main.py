import pcapkit
import pyshark
import socket
import netifaces as ni
#import scapy as sc
from scapy.all import IFACES



class InvalidChoice(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return f"Cannot find host: '{self.message}'"

class Analyze:

    def __init__(self, read_file):
        self.interface = self.get_net_interface()
        self.file = read_file

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

    def tcp_scan(self):
        print(f"getting TCP traffic data on interface {self.interface[0]} (IP: {self.interface[1]})")

        dst = f'ip.dst=={self.interface[1]} && tcp'
        print(dst)
        tcp_cap = pyshark.FileCapture(input_file=self.file, display_filter=dst)
        pack_count = 0
        
        #figure out better format for saving files to text for long term analysis
        tcp_file = open('./tcp_traffic.txt', 'a')
        while True:
            try:
                x = tcp_cap.next()
                # print(x.ip)
                tcp_file.write(str(x.ip))
                pack_count+=1
            except StopIteration:
                break

            try:
                print(x.ip, '\n')
            except AttributeError:
                pass
        print('TCP packets: ', pack_count)
        tcp_file.close()

    def udp_scan(self):
        print(f"getting UDP traffic data on interface {self.interface[0]} (IP: {self.interface[1]})")
        dst = f'ip.dst=={self.interface[1]} && udp'
        print(dst)
        udp_cap = pyshark.FileCapture(input_file=self.file, display_filter=dst)
        pack_count = 0
        
        #figure out better format for saving files to text for long term analysis
        udp_file = open('./udp_traffic.txt', 'a')
        while True:
            try:
                x = udp_cap.next()
                udp_file.write(str(x.ip))
                # print(x.ip)
                pack_count+=1
            except StopIteration:
                break

            try:
                print(x.ip, '\n')
            except AttributeError:
                pass
        print('UDP packets: ', pack_count)
        udp_file.close()


class main:

    while True:
        try:
            sniff_length = int(input("How many packets do you want to capture? "))
        except ValueError:
            print('Please input numeric value only.\n')
        else:
            break

    live = pyshark.LiveCapture(output_file='./scan_result.pcap').sniff(packet_count=sniff_length)
    # live.sniff(packet_count=sniff_length)

    a1 = Analyze('./scan_result.pcap')
    a1.tcp_scan()
    a1.udp_scan()
    

if __name__=="__main__":
    main()
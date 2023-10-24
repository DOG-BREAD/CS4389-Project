import pyshark
import socket
import netifaces as ni
from scapy.all import IFACES
import pandas as pd
from datetime import datetime
import subprocess
import os
import signal
import time
from dotenv import load_dotenv
load_dotenv()
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
        print(f"\ngetting TCP traffic data on interface {self.interface[0]} (IP: {self.interface[1]})")
        dst = f'ip.dst=={self.interface[1]} && tcp'
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
        have_header = False if os.path.exists('tcp_udp_scan.csv') else True
        df = pd.DataFrame(data)
        df.to_csv('tcp_udp_scan.csv', mode='a', index=False, header=have_header)
        print(df.head())

        # print(df.groupby(['source']))
        f = open('panda_write_tcp.txt', 'a')
        try:
            f.write(df.to_string())
        except:
            pass
        f.close()

    def udp_scan(self, read_file):
        print(f"\ngetting UDP traffic data on interface {self.interface[0]} (IP: {self.interface[1]})")
        dst = f'ip.dst=={self.interface[1]} && udp'
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
        df.to_csv('tcp_udp_scan.csv', mode='a', index=False, header=False)
        # print(df.groupby(['source']))
        
        f = open('panda_write_udp.txt', 'a')
        try:
            f.write(df.to_string())
        except:
            pass
        f.close()

    # Analyzes the specified IP address for possible port scanning
    # Calculates the duration of the scan, number of packets sent, and number of unique ports scanned
    def analyze_ip(self, file="tcp_udp_scan.csv", ip='127.0.0.1'):
        df = pd.read_csv(file)
        # Filter the DataFrame based on 'source' IP (Attacker)
        filtered_df = df[df['source'] == ip]
        # Get unique ports accessed by the specified source IP
        unique_ports = filtered_df['dst-port'].unique()
        unique_ports_df = pd.DataFrame(unique_ports,columns=["Ports"])
        if len(filtered_df) > 0:
            print("\n*** Possible Port Scanning Detected ***")
            print(f"---- Analyzing Scans Of IP: [{ip}] ----")
            df.loc[filtered_df.index, 'time'] = filtered_df['time']
            df_sorted = df.sort_values(by='time')
            # Get first and last entries
            first_scan = df_sorted.iloc[0]
            last_scan = df_sorted.iloc[-1]
            first_scan_time = first_scan['time']
            last_scan_time = last_scan['time']
            # Format of date string
            date_format = "%Y-%m-%d %H:%M:%S.%f"
            start_time = datetime.strptime(str(first_scan_time), date_format)
            end_time = datetime.strptime(str(last_scan_time), date_format)
            scan_duration = end_time - start_time
            print(f"Scan Duration: {scan_duration}")
            print(f'Number Of Packets Sent: {len(filtered_df)}')
            print(f'Number Of Unique Ports Scanned: {len(unique_ports)}')
            print(f'List of ports scanned: \n{unique_ports_df}\n')

    # Gets the unique IP addresses that sent packets to the specified host
    # If the IP sent more than 100 packets or scanned more than 10 unique ports, it is considered suspicious
    # All suspicious ips will be analyzed for possible port scanning
    def find_suspicious_ip(self, file="scan_result.pcap", ip='127.0.0.1'):  
        df = pd.read_csv("tcp_udp_scan.csv")
        unique_ip = df['source'].unique().tolist()
        try:
            unique_ip.remove('source')
        except ValueError:
            pass
        for _ip in unique_ip:
            filtered_df = df[df['source'] == _ip]
            unique_ports = filtered_df['dst-port'].unique()
            if (len(filtered_df) > 100) or (len(unique_ports) > 10):
                self.analyze_ip(ip=_ip)
            

class main:
    a1 = Analyze()
    # while True:
    #     try:
    #         sniff_length = int(input("How long (seconds) do you want to capture? "))
    #     except ValueError:
    #         print('Please input numeric value only.\n')
    #     else:
    #         break
    sniff_length=60
    print(f"sniffing for {sniff_length} seconds")
    live = pyshark.LiveCapture(interface= a1.interface[0],output_file=SCAN_FILE).sniff(timeout=sniff_length)
    print("done sniffing")
    a1.tcp_scan(SCAN_FILE)
    a1.udp_scan(SCAN_FILE)
    a1.find_suspicious_ip(ip=a1.interface[1])
    
if __name__=="__main__":
    main()
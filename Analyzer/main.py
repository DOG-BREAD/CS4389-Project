import pyshark
from pyshark.capture.capture import TSharkCrashException
import socket
import netifaces as ni
from scapy.all import IFACES
import pandas as pd
from datetime import datetime
import subprocess
import os
import time
from dotenv import load_dotenv
load_dotenv()
SCAN_FILE = './scan_result.pcap'

threat_list = pd.DataFrame(columns=['IP', 'First Packet Time', 'Last Packet Time','Duration', 'Min Port #','Max Port #', '# Unique Ports', '# Packets Sent'])

class InvalidChoice(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return f"Cannot find host: '{self.message}'"


# Method within Analyze to choose which network interface on a device to listen to.
# Made for devices with multiple interfaces (i.e. has VM network adapters)
# Returns a tuple of the format ('Interface Name', 'Interface IP')
def get_net_interface():
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
    select = dict(select)
    return select

def tcp_scan(inter, read_file):
    print(f"\ngetting TCP traffic data on interface {inter[0]} (IP: {inter[1]})")
    dst = f'ip.dst=={inter[1]} && tcp'
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

def udp_scan(inter, read_file):
    print(f"\ngetting UDP traffic data on interface {inter[0]} (IP: {inter[1]})")
    dst = f'ip.dst=={inter[1]} && udp'
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


# Analyzes the specified IP address for possible port scanning
# Calculates the duration of the scan, number of packets sent, and number of unique ports scanned
def analyze_ip(file="tcp_udp_scan.csv", ip='127.0.0.1'):
    df = pd.read_csv(file)
    # Filter the DataFrame based on 'source' IP (Attacker)
    filtered_df = df[df['source'] == ip]
    if len(filtered_df) > 0:
        print("\n*** Possible Port Scanning Detected ***")
        print(f"---- Analyzing Scans Of IP: [{ip}] ----")
        df.loc[filtered_df.index, 'time'] = filtered_df['time']
        df_sorted = filtered_df.sort_values(by='time')
        

        # Sorts the DataFrame by time and gets the unique times based on date and hour and significant digit of minute    
        df_sorted['time'] = pd.to_datetime(df_sorted['time'])
        df_sorted['unique_time'] = df_sorted['time'].dt.strftime('%Y-%m-%d %H:%M:%S.%f').str[:15]
        unique_times = df_sorted['unique_time'].unique()
        df_sorted = df_sorted.drop(columns=['unique_time'])
        
        for time in unique_times:
            test_df = df_sorted[df_sorted['time'].dt.strftime('%Y-%m-%d %H:%M:%S.%f').str[:15] == time]
            
            first_scan = test_df.iloc[0]
            first_scan_time = first_scan['time']
            last_scan = test_df.iloc[-1]
            last_scan_time = last_scan['time']
            unique_ports = test_df['dst-port'].unique()
            
            # Format of date string
            date_format = "%Y-%m-%d %H:%M:%S.%f"
            start_time = datetime.strptime(str(first_scan_time), date_format)
            end_time = datetime.strptime(str(last_scan_time), date_format)
            scan_duration = end_time - start_time
            threat_list.loc[len(threat_list)] = [
                ip,
                first_scan_time,
                last_scan_time,
                scan_duration,
                unique_ports.min(),
                unique_ports.max(),
                len(unique_ports),
                len(test_df)
            ]


# Gets the unique IP addresses that sent packets to the specified host
# If the IP sent more than 100 packets or scanned more than 10 unique ports, it is considered suspicious
# All suspicious ips will be analyzed for possible port scanning
def find_suspicious_ip(file="scan_result.pcap", ip='127.0.0.1'):  
    try:
        df = pd.read_csv("tcp_udp_scan.csv")
    except:
        print("Column headers not found. Exiting...")
        return    
    unique_ip = df['source'].unique().tolist()
    try:
        unique_ip.remove('source')
    except ValueError:
        pass
    for _ip in unique_ip:
        filtered_df = df[df['source'] == _ip]
        unique_ports = filtered_df['dst-port'].unique()
        if ((len(filtered_df) > 100) or (len(unique_ports) > 10)) and (filtered_df['destination'].unique()[0] == ip):
            analyze_ip(ip=_ip)
 
def get_threat_list():
    return threat_list

def clear_threat_list():
    global threat_list
    threat_list = pd.DataFrame(columns=['IP', 'First Packet Time', 'Last Packet Time','Duration', 'Min Port #','Max Port #', '# Unique Ports', '# Packets Sent'])

def run_cleanup():
    # Clean up the csv file by removing all rows besides the headers
    print("cleaning up csv")
    df = pd.read_csv('tcp_udp_scan.csv')
    # Keep the first row as the header
    
    headers = df.columns
    df = pd.DataFrame(columns=headers)

    # Save the cleaned up csv file
    df.to_csv('tcp_udp_scan.csv', index=False, header=True)
    print("done cleaning up csv")

  
def driver(inter):
    sniff_length = 10
    
    print(f'inteface: {inter}')
    print(f"sniffing for {sniff_length} seconds")
    live = pyshark.LiveCapture(interface= inter[0],output_file=SCAN_FILE).sniff(timeout=sniff_length)
    print("done sniffing")
    tcp_scan(inter, SCAN_FILE)
    udp_scan(inter, SCAN_FILE)
    find_suspicious_ip(ip=inter[1])
    try:
        data = pd.read_csv("tcp_udp_scan.csv")
        if len(data) > 10000:
            run_cleanup()
    except:
        pass
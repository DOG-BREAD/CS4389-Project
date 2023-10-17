import pyshark
import scapy.all as scapy

# parse the pcap file with regex --> later
def parse_pcap_with_regex(file_path, pattern):
    packets = scapy.rdpcap(file_path)

    for packet in packets:
        # Convert packet data to a string
        packet_data_str = str(packet)
        
        # Apply the regex pattern
        matches = re.findall(pattern, packet_data_str)
        
        # Process the matches as needed
        for match in matches:
            print(match)


# packets = enumerate(scapy.rdpcap('test.pcap'))
file = open('plain.txt', 'a')

#load the file into list format 
packets = scapy.rdpcap('scan_result.pcap')
start_time = packets[0].time # start packet time
for x, pack in enumerate(packets):
    #enumerated packet number , packet information and delta from start time
    pack_str = f'packet#{x}: {str(pack)} time:{str(pack.time - start_time) }'
    print(pack_str)
    file.write(pack_str)
    file.write("\n")

#close the file 
file.close
# testfile = open('./test.txt', 'a')
# pack_count = 0
# while True:
#     try:
#         x = testcap.next()
#         # print(x.ip)
#         testfile.write(x.ip)
#         pack_count+=1
#     except StopIteration:
#         break
#     try:
#         print(str(x.ip), '\n')
#     except AttributeError:
#         pass
# print('TCP packets: ', pack_count)
# testfile.close()
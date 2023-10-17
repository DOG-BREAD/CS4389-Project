import pyshark
import scapy.all as scapy

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


testcap =  pyshark.LiveCapture(interface='Wi-Fi', output_file='test.pcap')
testcap.sniff(timeout=3)

packets = enumerate(scapy.rdpcap('test.pcap'))
# packets = scapy.rdpcap('test.pcap')
start_time = packets.__next__[1].time

for x, pack in packets:

    pack_str = f'packet#{x}: {str(pack)} time:{str(pack.time - start_time)}'
    print(pack_str)

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
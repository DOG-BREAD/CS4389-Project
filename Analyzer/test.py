import pyshark

testcap =  pyshark.LiveCapture(interface='Wi-Fi', only_summaries=True)
testcap.sniff(packet_count=50)
testfile = open('./test.txt', 'a')
pack_count = 0
while True:
    try:
        x = testcap.next()
        # print(x.ip)
        testfile.write(x.frame_info)
        pack_count+=1
    except StopIteration:
        break
    try:
        print(str(x.ip), '\n')
    except AttributeError:
        pass
print('TCP packets: ', pack_count)
testfile.close()
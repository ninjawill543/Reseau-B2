from scapy.all import sniff, ICMP

def print_it_please(packet):
    if (packet['ICMP'].type == 0):
        print(packet['Raw'].load)

sniff(filter="icmp", prn=print_it_please, count=0)

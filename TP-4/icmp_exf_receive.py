from scapy.all import sniff

def print_it_please(packet):
    print(packet)

sniff(filter="icmp", prn=print_it_please, count=0)

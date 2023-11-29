from scapy.all import sniff, ICMP

def print_it_please(packet):
    if (packet['ICMP'].type == 8 and len(packet['Raw'].load) == 1):
        print(packet['Raw'].load)
        quit()

sniff(filter="icmp", prn=print_it_please, count=0)

#iface="" if you want to change interface for the sniff

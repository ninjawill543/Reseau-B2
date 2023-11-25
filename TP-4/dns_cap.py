from scapy.all import sniff, DNS

def print_ip_address(packet):
    if DNS in packet and packet[DNS].qr == 1: 
        for answer in packet[DNS].an:
            print(answer.rdata)

sniff(filter="udp and port 53", prn=print_ip_address, count=2)


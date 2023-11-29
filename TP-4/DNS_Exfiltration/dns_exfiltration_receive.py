from scapy.all import *

received_packets = {}

def dns_sniff(packet):
    global received_packets
    if DNS in packet and packet.dport == 53 and packet[DNS].qr == 0:
        domain_name = packet[DNSQR].qname.decode('utf-8')
        domain_name = domain_name.replace('°', '.')
        if "~~end~~" in domain_name:
            sorted_packets = ''.join(value for key, value in sorted(received_packets.items()))
            print(sorted_packets.replace('°', '.'))
            quit()
        elif "~" in domain_name and not "~~end~~" in domain_name:
            index = domain_name.find("~")
            packet_count = int(domain_name[:index])
            substring = domain_name[index + 1:-19]
            received_packets[packet_count] = substring

sniff(filter='udp port 53', prn=dns_sniff)


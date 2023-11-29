from scapy.all import *

unique_strings = {}

def dns_sniff(packet):
    global unique_strings
    if DNS in packet and packet.dport == 53 and packet[DNS].qr == 0:
        domain_name = packet[DNSQR].qname.decode('utf-8')
        if "~~end~~" in domain_name:
            sorted_strings = ''.join(value for key, value in sorted(unique_strings.items()))
            print(sorted_strings)
            quit()
        elif "~" in domain_name and not "~~end~~" in domain_name:
            index = domain_name.find("~")
            packet_count = int(domain_name[:index])
            substring = domain_name[index + 1:-18]

            # Add packet count and substring to the dictionary
            unique_strings[packet_count] = substring

sniff(filter='udp port 53', prn=dns_sniff)


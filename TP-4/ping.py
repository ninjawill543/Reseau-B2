from scapy.all import *

ping = ICMP(type=8)

packet = IP(src="10.33.72.7", dst="10.33.76.225")

frame = Ether(src="b0:3c:dc:ae:ab:6e", dst="d8:f3:bc:54:c7:8f")

final_frame = frame/packet/ping

answers, unanswered_packets = srp(final_frame, timeout=10)

print(f"Pong reçu : {answers[0]}")


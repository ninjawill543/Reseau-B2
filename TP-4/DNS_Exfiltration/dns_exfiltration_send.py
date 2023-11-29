from scapy.all import *
import sys


def dns_send(query_domain, dns_server="lucashanson.tech"):
    dns_request = Ether()/IP(dst=dns_server)/UDP(dport=53)/DNS(rd=1, qd=DNSQR(qname=query_domain))
    answers, unanswered_packets = srp(dns_request, timeout=2, verbose=False)


domain_to_query = sys.argv[1] + ".lucashanson.tech"
#domain_to_query = "lucashanson.tech"
dns_send(domain_to_query)


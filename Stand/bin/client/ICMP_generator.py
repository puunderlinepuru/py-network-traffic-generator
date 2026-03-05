from scapy.all import *
import random

ip_src_normal = "127.0.0.1"
ip_src_sus = "127.0.0.1"
ip_dst = "127.0.0.1"
tos_normal = 8
tos_sus = 7

if len(sys.argv) < 3:
    count = 30
    sus_packets_amount = 0
else:
    count = int(sys.argv[1])
    sus_packets_amount = int(sys.argv[2])
print(f'capturing {count} packets')


def send_icmp(dest_ip, tos=0, src_ip="192.168.1.1", id=random.randint(1, 65535)):
    # Create an ICMP packet with the required fields
    icmp = IP(dst=dest_ip, tos=tos, src=src_ip, id=id)/ICMP()/"Hello, World!"

    # Send the packet and get the response
    resp = sr1(icmp)

    if resp:
        print("Received ICMP reply from", dest_ip)
    else:
        print("No response received.")

sus_packets_index_start = random.randint(1,count-sus_packets_amount)
print("injecting at ", sus_packets_index_start)

if (count-sus_packets_amount - sus_packets_index_start == 0):
    for _ in range(sus_packets_index_start):
        send_icmp(dest_ip=ip_dst, tos=tos_normal, src_ip=ip_src_normal)
    for _ in range(sus_packets_amount):
        send_icmp(dest_ip=ip_dst, tos=tos_sus, src_ip=ip_src_sus)

else:
    for _ in range(sus_packets_index_start):
        send_icmp(dest_ip=ip_dst, tos=tos_normal, src_ip=ip_src_normal)
    for _ in range(sus_packets_amount):
        send_icmp(dest_ip=ip_dst, tos=tos_sus, src_ip=ip_src_sus)
    for _ in range(count - (sus_packets_index_start + sus_packets_amount)):
        send_icmp(dest_ip=ip_dst, tos=tos_normal, src_ip=ip_src_normal)

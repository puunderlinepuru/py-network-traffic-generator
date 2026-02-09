from scapy.all import *
import json

print("Starting sniffer...")

# Sniff 5 packets and then stop
packets = sniff(count=5, iface="Ethernet")

print("Sniffing complete. Packets captured:")
packets.summary()
json_packet = packets[0].json()
packet_disass = json.loads(json_packet)

# try:
#     print(packet_disass["id"])
# except:
#     print("wrong")


choice = input("Press Enter to exit")
while choice != "":
    if choice == "packet":
        print(packet_disass)
    elif choice == "stega":
        # print(packet_disass["src"])
        # print(packet_disass["tos"])
        print(packet_disass['payload']['id'])
    choice = input("Press Enter to exit")
# importing csv
import csv
from scapy.all import *
import json

data = [[]]

print("Starting sniffer...")

# Sniff 5 packets and then stop
packets = sniff(prn=lambda x: x.summary(), count=100, iface="Ethernet")

print("Sniffing complete. Packets captured:")
# packets.summary()
# json_packet = packets[0].json()
# packet_disass = json.loads(json_packet)


for packet in packets:
    json_packet = packet.json()
    packet_disass = json.loads(json_packet)
    data.append([packet_disass['src'], packet_disass['dst'], packet_disass['payload']['id']])

# try:
#     print(packet_disass["id"])
# except:
#     print("wrong")


# choice = input("Press Enter to exit")
# while choice != "":
#     if choice == "packet":
#         print(packet_disass)
#     elif choice == "stega":
#         print(packet_disass["src"])
#         print(packet_disass["tos"])
#         print(packet_disass['payload']['id'])
#     choice = input("Press Enter to exit")

# File path for the CSV file
csv_file_path = 'example.csv'

# Open the file in write mode
with open(csv_file_path, mode='w', newline='') as file:
    # Create a csv.writer object
    writer = csv.writer(file)
    # Write data to the CSV file
    writer.writerows(data)

# Print a confirmation message
print(f"CSV file {csv_file_path} created successfully")
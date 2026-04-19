

import sys
import csv
from scapy.all import *
from scapy.layers.inet import IP, TCP, ICMP
import json

# File path for the CSV file
csv_file_path = f"generated/capture.csv"
json_file_path = f"generated/capture.json"

# Source - https://stackoverflow.com/a/24196955
# Posted by Martin Konecny, modified by community. See post 'Timeline' for change history
# Retrieved 2026-03-30, License - CC BY-SA 4.0


# Define whether script is run from PC or Laptop
if (sys.argv[1] == 'pc'):
    interface = 'Подключение по локальной сети'
elif (sys.argv[1] == 'pc_local'):
    interface = 'Inner Ethernet'
elif (sys.argv[1] == 'laptop'):
    interface = 'wlan0'
elif (sys.argv[1] == 'laptop_local'):
    interface = 'lo'

script_path = sys.argv[0]
script_directory = os.path.dirname(os.path.abspath(script_path))

resource_path = script_directory + r'/generated'
if not os.path.exists(resource_path):
    os.makedirs(resource_path)

print("Starting sniffer...")

if len(sys.argv) < 3:
    count = 100
else:
    count = int(sys.argv[2])
print(f'capturing {count} packets')

port = 12345
# TCP
packets = sniff(prn=lambda x: x.summary(), filter=f"tcp", count=count, iface=interface)

# ICMP
# packets = sniff(prn=lambda x: x.summary(), filter=f"icmp and src not 192.168.0.12", count=count, iface=interface)

# UDP
# packets = sniff(prn=lambda x: x.summary(), filter=f"udp and src 10.235.118.137", count=count, iface=interface)

print("Sniffing complete.")

data = []
json_packet = packets[0][IP].json()
packet_disass = json.loads(json_packet)
packet_fields = packet_disass.keys()



json_packets = []

with open(json_file_path, mode='w', encoding='utf-8') as json_file:
    json.dump(json_packets, json_file, indent=4)

with open(csv_file_path, mode='w', newline='') as csv_file:
    # Create a csv.writer object
    writer = csv.writer(csv_file)
    # Write data to the CSV file
    writer.writerow(packet_fields)

    for packet in packets:
        json_packet = packet[IP].json()
        packet_disass = json.loads(json_packet)
        json_packets.append(packet_disass)
        
        writer.writerow(packet_disass.values())
    



# Open the file in write mode

# Print a confirmation message
print(f"CSV file {csv_file_path} created successfully")


import sys
import csv
from scapy.all import *
import json

# Define whether script is run from Win or Linux
if (sys.argv[1] == 'pc'):
    interface = 'Ethernet'
elif (sys.argv[1] == 'laptop'):
    interface = 'wlan0'

data = [["src", "dst", "id", "checksum", "ipv4_src"]]

print("Starting sniffer...")

count = int(sys.argv[2]) or 100
print(f'capturing {count} packets')


packets = sniff(prn=lambda x: x.summary(), count=count, iface=interface)

print("Sniffing complete. Packets captured:")


for packet in packets:
    json_packet = packet.json()
    packet_disass = json.loads(json_packet)
    try:
        data.append([packet_disass['src'], packet_disass['dst'], packet_disass['payload']['id'], packet_disass['payload']['chksum'],packet_disass['payload']['src']])
    except:
        print('ERROR')
        print(packet_disass)


# choice = input("Press Enter to exit")
# while choice != "":
#     if choice == "packet":
#         print(packet_disass)
#     elif choice == "stega":
#         print(packet_disass["src"])
#         print(packet_disass["tos"])
#         print(packet_disass['payload']['id'])
#     choice = input("Press Enter to exit")

resource_path = r'./generated'
if not os.path.exists(resource_path):
    os.makedirs(resource_path)

# File path for the CSV file
csv_file_path = f"generated/capture.csv"

# Open the file in write mode
with open(csv_file_path, mode='w', newline='') as file:
    # Create a csv.writer object
    writer = csv.writer(file)
    # Write data to the CSV file
    writer.writerows(data)

# Print a confirmation message
print(f"CSV file {csv_file_path} created successfully")
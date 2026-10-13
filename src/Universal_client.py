import ICMPv4_generator
import TCP_client

menu_choice = int(input(
    "Menu" \
    "\n[1] Generate ICMP" \
    "\n[2] Initiate TCP" \
    "\nchoice: "))

# 
while(menu_choice != 0):
    # ICMP
    if(menu_choice == 1):
        submenu_choice = int(input(
        "\n\nICMP Generation" \
        "\n[1] Source IP" \
        "\n[2] ToS" \
        "\nchoice: "))

        # Source IP
        if(submenu_choice == 1):
            count = int(input("count: "))
            stego_amount = int(input("bad packets: "))
            normal_src = input("Normal Source IP:")
            stego_src = input("Changed Source IP:")
            dst = input("Destination IP: ")
            normal_tos = int(input("ToS: "))
            ICMPv4_generator.generate_traffic_src_ip(count,stego_amount,normal_src,stego_src,dst, normal_tos)
        
        # ToS
        if(submenu_choice == 2):
            count = int(input("count: "))
            stego_amount = int(input("bad packets: "))
            normal_src = input("Source IP:")
            dst = input("Destination IP: ")
            normal_tos = int(input("Normal ToS: "))
            stego_tos = int(input("Changed ToS: "))
            ICMPv4_generator.ICMP_generate_traffic_tos(count, stego_amount, normal_src, dst, normal_tos, stego_tos)

    if(menu_choice == 2):
        submenu_choice = int()

    menu_choice = int(input(
    "\n\nMenu" \
    "\n[1] Generate ICMP" \
    "\n[2] Initiate TCP" \
    "\nchoice: "))
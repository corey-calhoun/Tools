####################################################################################################
# Description: This script scans the network and arp table for devices
# and then returns the properties of the device in a table.
# Author: tr4shp4nd4
# Date: 03/03/2023
#
# Usage: python3 device_find.py
####################################################################################################

import re
import platform
import socket
import subprocess
from urllib import request

def get_arp_table() -> list:
    os_name = platform.system()
    if os_name == "Windows":
        arp_table = subprocess.check_output("arp -a", shell=True)
        arp_table = arp_table.decode("utf-8").split("\n")
    elif os_name == "Linux":
        arp_table = subprocess.check_output("arp -a", shell=True)
        arp_table = arp_table.decode("utf-8").split("\n")
    else:
        return []
    return arp_table

def get_mac_vendor(mac: str) -> str:
    url = "https://api.macvendors.com/" + mac
    try:
        vendor = request.urlopen(url).read().decode("utf-8")
    except:
        vendor = ""
    return vendor

def get_device_info(ip: str, mac: str) -> list:
    try:
        hostname = socket.gethostbyaddr(ip)[0]
    except:
        hostname = ""
    vendor = get_mac_vendor(mac)
    return [ip, mac, hostname, vendor]

def main():
    arp_table = get_arp_table()
    devices = []
    for i in arp_table:
        if re.search("([0-9a-f]{2}[:-]){5}([0-9a-f]{2})", i):
            parts = i.split()
            ip = parts[0]
            mac = parts[1]
            device_info = get_device_info(ip, mac)
            devices.append(device_info)
    print('{:<15} {:<20} {:<30} {:<50}'.format('IP Address', 'MAC Address', 'Device Name', 'Device Vendor'))
    for device in devices:
        print('{:<15} {:<20} {:<30} {:<50}'.format(device[0], device[1], device[2], device[3]))

if __name__ == "__main__":
    main()
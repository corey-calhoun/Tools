####################################################################################################
# Description: This script runs 'nmap -sC -sV -T4 <ip> -oN magicscan.txt' with <ip> being an arg.
# The results are then displayed in a table format and saved to a file.
# The results are then parsed for the open ports and the services running on those ports.
# The services are then used to search for exploits. The exploits are then displayed in a table.
#
# Author: tr4shp4nd4
# Date: 03/03/2023
#
# Usage: python3 starter.py <ip>
####################################################################################################

import re # Regular expressions
import sys # System-specific parameters and functions
import subprocess # Subprocess management
import requests # HTTP for Humans
from bs4 import BeautifulSoup # Screen-scraping library

# Function to run nmap scan 'nmap -sC -sV -T4 <ip> -oN magicscan.txt'
def run_nmap_scan(ip: str) -> str:
    nmap_scan = subprocess.check_output("nmap -sC -sV -T4 " + ip + " -oN magicscan.txt", shell=True)
    nmap_scan = nmap_scan.decode("utf-8")
    return nmap_scan

# Function to parse nmap scan results
def parse_nmap_scan(nmap_scan: str) -> list:
    ports = []
    services = []
    for i in nmap_scan.split("\n"):
        if re.search("open", i):
            port = i.split("/")[0]
            service = i.split("/")[2]
            ports.append(port)
            services.append(service)
    return ports, services

# Function to search exploit-db for exploits
def search_exploit_db(services: list) -> list:
    exploits = []
    for service in services:
        url = "https://www.exploit-db.com/search?q=" + service
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        for i in soup.find_all("a", href=True):
            if re.search("exploits", i["href"]):
                exploits.append(i["href"])
    return exploits

# Function to parse exploit-db results
def parse_exploit_db(exploits: list) -> list:
    exploit_info = []
    for exploit in exploits:
        url = "https://www.exploit-db.com" + exploit
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        for i in soup.find_all("div", class_="exploit_list"):
            exploit_info.append(i.text)
    return exploit_info

# Function to display results in a table
def display_results(ports: list, services: list, exploit_info: list) -> None:
    print('{:<15} {:<20} {:<30}'.format('Port', 'Service', 'Exploit'))
    for i in range(len(ports)):
        print('{:<15} {:<20} {:<30}'.format(ports[i], services[i], exploit_info[i]))
    
# Main function
def main():
    ip = sys.argv[1]
    nmap_scan = run_nmap_scan(ip)
    ports, services = parse_nmap_scan(nmap_scan)
    exploits = search_exploit_db(services)
    exploit_info = parse_exploit_db(exploits)
    display_results(ports, services, exploit_info)

if __name__ == "__main__":
    main()

# EOF

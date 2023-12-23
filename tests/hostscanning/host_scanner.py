import ipaddress
import socket

def list_hosts_in_network(network):
    print(f"Listing hosts in the network: {network}")

    for ip in ipaddress.IPv4Network(network, strict=False).hosts():
        try:
            host_name = socket.gethostbyaddr(str(ip))
        except (socket.herror, socket.gaierror):
            host_name = "N/A"
        print(f"Host IP: {ip}, Hostname: {host_name}")

# Scanning the specific network '192.168.1.0/24'
specific_network = "192.168.1.0/24"
list_hosts_in_network(specific_network)



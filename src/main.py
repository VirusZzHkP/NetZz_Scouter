import socket
import ipaddress
import subprocess
import netifaces as ni
import requests
from datetime import datetime
import time


def banner():
    banner_text = r""".##..##..######..######..######..######...........####....####....####...##..##..######..######..#####..
.###.##..##........##.......##......##...........##......##..##..##..##..##..##....##....##......##..##.
.##.###..####......##......##......##.............####...##......##..##..##..##....##....####....#####..
.##..##..##........##.....##......##.................##..##..##..##..##..##..##....##....##......##..##.
.##..##..######....##....######..######...........####....####....####....####.....##....######..##..##."""
    line_1 = "GitHub: @VirusZzHkP  || YouTube: @JustHack_IT"
    line_2 = "M@d3 With Love - VirusZzWarning"
	
    # Calculate the spaces needed to center the lines
    spaces_top = (104 - len(line_1)) // 2
    spaces_mid = (104 - len(line_2)) // 2

    print("=" * 104)
    print(" " * spaces_top + line_1)
    print("=" * 104)
    print(banner_text)
    print("=" * 104)
    print(" " * spaces_mid + line_2)
    print("-" * 104)




def get_open_ports(target_ip, ports, animate=True):
    open_ports = []
    total_ports = len(ports)
    progress_step = 1 if total_ports == 0 else max(total_ports // 10, 1)  # Adjust animation frequency

    for i, port in enumerate(ports):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((target_ip, port))
        if result == 0:
            open_ports.append(port)
        
        sock.close()
    
    if animate:
        print("Scanning... [100% complete]")
    
    return open_ports

def scan_specific_device():
    
    
    target_ip = input("Enter the target IP address or hostname: ")
    try:
        target_ip = socket.gethostbyname(target_ip)
    except socket.gaierror:
        print("Invalid IP address or hostname.")
        return

    # Get the port scanning option
    ports_option = input("Select a port scanning option:\n1. Specific port\n2. Scan all ports\n")

    if ports_option == '1':
        # Scan a specific port
        port_to_scan = input("Enter the port to scan: ")
        try:
            port_to_scan = int(port_to_scan)
            if port_to_scan < 1 or port_to_scan > 65535:
                print("Port number out of range. Please enter a valid port (1-65535).")
                return
        except ValueError:
            print("Invalid port number. Please enter a valid port (1-65535).")
            return

        # Scan the specified port
        ports = [port_to_scan]
        print("Scanning port %d..." &port_to_scan)
        open_ports = get_open_ports(target_ip, ports)

        if open_ports:
            print("Port is open on the target.")
        else:
            print("Port is closed on the target.")
    elif ports_option == '2':
        # Scan all ports
        ports = list(range(1, 65536))
        print("Scanning all ports...")
        open_ports = get_open_ports(target_ip, ports)

        if open_ports:
            print("Open ports on the target:")
            for i, port in enumerate(open_ports, start=1):
                print("{}. {}".format(i, port))
        else:
            print("No open ports found.")
    else:
        print("Invalid option.")
    
    print("Scan completed.")


def scan_network_automatically():
    
    
    try:
        gateway_ip = ni.gateways()['default'][ni.AF_INET][0]
        network = ni.ifaddresses(ni.gateways()['default'][ni.AF_INET][1])[ni.AF_INET][0]['addr']
        network = ".".join(network.split('.')[:3]) + ".0/24"
    except:
        print("Unable to detect your network. Please enter the network manually.")
        return

    # Display the detected IP and confirm with the user
    print(f"Detected IP address: {network}")
    confirm = input("Is this the correct IP address for your network? (yes/no): ")
    
    if confirm.lower() != "yes":
        print("Aborted. Please enter the network manually.")
        return

    ports_option = input("Select a port scanning option:\n1. Specific ports\n2. Scan all ports\n")
    if ports_option == '1':
        ports_input = input("Enter the ports to scan (e.g., 80,443,8080): ")
        if ports_input:
            ports = [int(port.strip()) for port in ports_input.split(',')]
        else:
            ports = []
    elif ports_option == '2':
        ports = list(range(1, 65536))
    else:
        print("Invalid option.")
        return

    num_hosts = 0
    open_ports_count = 0

    for ip in ipaddress.IPv4Network(network, strict=False).hosts():
        num_hosts += 1
        open_ports = get_open_ports(str(ip), ports)
        if open_ports:
            open_ports_count += 1
            print(f"Open ports on {ip}:")
            for i, port in enumerate(open_ports, start=1):
                print(f"{i}. {port}")
    
    print(f"Scanned {num_hosts} hosts. Found open ports on {open_ports_count} hosts.")
    print("Scan completed.")
    
def list_hosts_in_network(network):
    banner()
    print(f"Listing hosts in the network: {network}")

    for ip in ipaddress.IPv4Network(network, strict=False).hosts():
        try:
            host_name = socket.gethostbyaddr(str(ip))
        except (socket.herror, socket.gaierror):
            host_name = "N/A"
        print(f"Host IP: {ip}, Hostname: {host_name}")

def display_status_codes():
    print("Important Status Codes and their Meanings:")
    print("=========================================")
    print("100: Continue - The server has received the request headers and the client should proceed to send the request body.")
    print("200: OK - The request was successful.")
    print("300: Multiple Choices - The server has several possible responses and the user or user agent can choose one.")
    print("400: Bad Request - The server cannot process the request due to a client error.")
    print("403: Forbidden - The server understood the request but refuses to authorize it.")
    print("404: Not Found - The requested resource could not be found on the server.")
    print("500: Internal Server Error - The server encountered an unexpected condition that prevented it from fulfilling the request.")
    print("502: Bad Gateway - The server, while acting as a gateway or proxy, received an invalid response from the upstream server.")
    print("503: Service Unavailable - The server is currently unavailable (overloaded or down for maintenance).")
    print("\n")

def porthit():
    display_status_codes()
    
    while True:
        host = input("Enter the website URL to monitor (e.g., example.com): ")
        port = input("Enter the port to monitor (e.g., 80): ")

        last_status = None
        last_err = ''
        ping_count = 0
        
        try:
            while True:
                try:
                    start_time = datetime.now()
                    resp = requests.get(f"http://{host}:{port}", timeout=5)
                    end_time = datetime.now()

                    if resp.status_code != last_status:
                        print(f"{end_time.isoformat()}: Website is {resp.reason} ({resp.status_code})")
                        last_status = resp.status_code
                        last_err = ''
                    else:
                        print(f"{end_time.isoformat()}: Website status remains {resp.reason} ({resp.status_code})")
                    
                    ping_count += 1
                    if ping_count % 10 == 0:
                        decision = input("Do you want to continue? (Press Enter to continue, type 'stop' to halt scanning): ")
                        if decision.lower() == 'stop':
                            print("Monitoring stopped.")
                            return
                except Exception as e:
                    if str(e) != last_err:
                        print(f"{datetime.now().isoformat()}: Connection error ({str(e)})")
                        last_err = str(e)
                        last_status = None
                
                time.sleep(2)  # Wait for 2 seconds before the next ping

        except KeyboardInterrupt:
            print("\nMonitoring stopped.")
            break


def main():
    while True:
        banner()
        print("1. Scan a specific device")
        print("2. Scan the local network automatically")
        print("3. List all hosts in the network")
        print("4. Ping a website")
        option = input("Select an option (1/2/3/4): ")
        print("-" * 104)

        if option == '1':
            scan_specific_device()
        elif option == '2':
            scan_network_automatically()
        elif option == '3':
            try:
                gateway_ip = ni.gateways()['default'][ni.AF_INET][0]
                network = ni.ifaddresses(ni.gateways()['default'][ni.AF_INET][1])[ni.AF_INET][0]['addr']
                network = ".".join(network.split('.')[:3]) + ".0/24"
                list_hosts_in_network(network)
            except:
                print("Unable to list hosts. Please enter the network manually.")
        elif option == '4':
            porthit()
        else:
            print("Invalid option.")
        
        repeat = input("Back to main menu (yes/no): ")
        if repeat.lower() != "yes":
            print("Thank you for using the tool.")
            print("M@d3 With <3 - VirusZzWarning")
            break

if __name__ == "__main__":
    main()


import socket

def scan_ports(host, ports):
    print(f"Scanning {host} for ports: {ports}")
    for port in ports:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                result = s.connect_ex((host, port))
                if result == 0:
                    print(f"[+] Port {port} is open")
        except Exception as e:
            print(f"Error on port {port}: {e}")

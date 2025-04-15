from port_scanner import scan_ports
from brute_forcer import brute_force_login

def run_toolkit():
    print("=== Penetration Testing Toolkit ===")
    
    # Port Scanning
    target = input("Enter target IP (e.g., 127.0.0.1): ")
    ports = [21, 22, 23, 80, 443]
    scan_ports(target, ports)

    # Brute Force
    url = input("Enter login URL: ")
    user = input("Username to brute-force: ")
    password_list = ["admin", "123456", "password", "letmein"]
    brute_force_login(url, user, password_list)

if __name__ == "__main__":
    run_toolkit()

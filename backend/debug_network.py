
import socket
import os
from dotenv import load_dotenv
from urllib.parse import urlparse

load_dotenv()

def check_connectivity():
    url_str = os.getenv("DATABASE_URL")
    if not url_str:
        print("DATABASE_URL not found.")
        return

    # Extract host
    if "@" in url_str:
        host_part = url_str.split("@")[-1]
        host = host_part.split(":")[0]
        port = 5432
        if ":" in host_part:
            try:
                # Handle host:port/db
                port_str = host_part.split(":")[1].split("/")[0]
                port = int(port_str)
            except:
                pass
    else:
        print("Could not parse host from URL")
        return

    print(f"Target Host: {host}")
    print(f"Target Port: {port}")

    print("\n--- DNS Resolution ---")
    try:
        ais = socket.getaddrinfo(host, port)
        for result in ais:
            family, _, _, _, sockaddr = result
            ip = sockaddr[0]
            fam_str = "IPv6" if family == socket.AF_INET6 else "IPv4"
            print(f"Resolved {fam_str}: {ip}")
    except Exception as e:
        print(f"DNS Resolution failed: {e}")

    print("\n--- Connectivity Test (IPv4) ---")
    try:
        ipv4_ip = socket.gethostbyname(host) # This usually prefers IPv4
        print(f"Testing connection to {ipv4_ip}:{port}...")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(3)
        s.connect((ipv4_ip, port))
        print("SUCCESS: Connected via IPv4")
        s.close()
    except Exception as e:
        print(f"FAILURE: Could not connect via IPv4: {e}")

if __name__ == "__main__":
    check_connectivity()

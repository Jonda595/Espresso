import socket

target = input("Cíl (IP/doména): ")

ports = input("Range: ")

print(f"\nScanning {target}...\n")

for port in range(int(ports)):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.2)

    try:
        s.connect((target, port))
        print(f"[OPEN]   {port}")
    except (socket.timeout, ConnectionRefusedError, OSError):
        print(f"[CLOSED/FILTERED] {port}")
    finally:
        s.close()

print("\nScan complete.")

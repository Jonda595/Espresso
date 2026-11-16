import time
import random

HOSTS = {
    "gateway": {
        "ip": "192.168.56.1",
        "ports": [22, 80],
        "users": {
            "admin": "lab-gateway-42",
            "operator": "welcome1"
        }
    },
    "web": {
        "ip": "192.168.56.10",
        "ports": [22, 80, 443],
        "users": {"dev": "orange-cactus-73"}
    },
    "files": {
        "ip": "192.168.56.20",
        "ports": [22, 21],
        "users": {
            "backup": "winter-lab-2026",
            "analyst": "blue-team-19"
        }
    },
    "db": {
        "ip": "192.168.56.30",
        "ports": [22, 5432],
        "users": {
            "postgres": "db-lab-2026",
            "dba": "cobalt-bridge-55"
        }
    }
}

VULNERABILITIES = {
    "web": {
        "CVE-2021-41773": {
            "name": "Apache Path Traversal",
            "severity": "CRITICAL",
            "vulnerable": True
        }
    },
    "gateway": {
        "CVE-2023-0001": {
            "name": "Simulated SSH Authentication Flaw",
            "severity": "HIGH",
            "vulnerable": True
        }
    }
}

FILES = {
    "/": ["etc", "home", "var", "tmp"],
    "/etc": ["hostname", "hosts", "passwd"],
    "/home": ["user"],
    "/home/user": ["notes.txt", "todo.txt"],
    "/var": ["log"],
    "/var/log": ["auth.log", "system.log"],
    "/tmp": []
}

CONTENTS = {
    "/etc/hostname": "ironclad-lab",
    "/etc/hosts": "127.0.0.1 localhost\n192.168.56.1 gateway",
    "/etc/passwd": "root:x:0:0:root:/root:/bin/sh\nuser:x:1000:1000:user:/home/user:/bin/sh",
    "/home/user/notes.txt": "Welcome to IRONCLAD.\nThis is a simulated cyber range.",
    "/home/user/todo.txt": "1. Scan the lab\n2. Inspect services\n3. Review logs",
    "/var/log/auth.log": "Accepted password for admin\nFailed login for guest",
    "/var/log/system.log": "System boot completed\nNetwork interface initialized"
}

current_host = "localhost"
current_dir = "/"
history = []


def pause():
    time.sleep(0.4)


def banner():
    print("""
=================================
          IRONCLAD
       CYBER RANGE SIMULATOR
=================================
Type 'help' for commands.
""")


def resolve_host(target):
    if target in HOSTS:
        return HOSTS[target]["ip"]

    for name in HOSTS:
        if HOSTS[name]["ip"] == target:
            return target

    return None


def scan(target, version=False):
    host = None

    for name in HOSTS:
        if name == target or HOSTS[name]["ip"] == target:
            host = HOSTS[name]
            break

    if host is None:
        print("Host seems down.")
        return

    print("Starting simulated scan...")
    pause()
    print("Host is up.")
    print("PORT     STATE     SERVICE")

    for port in host["ports"]:
        service = {
            22: "ssh",
            80: "http",
            443: "https",
            21: "ftp",
            5432: "postgresql"
        }.get(port, "unknown")

        print(str(port) + "/tcp  open      " + service)

        if version:
            print("         Version: simulated-" + service + "-1.0")


def ssh(hostname):
    if hostname not in HOSTS:
        print("Unknown host.")
        return

    username = input("Username: ")
    password = input("Password: ")

    users = HOSTS[hostname]["users"]

    if users.get(username) == password:
        print("Authentication successful.")
        print("Connected to " + hostname)

        global current_host
        current_host = hostname
    else:
        print("Permission denied.")


def exploit(host, cve):
    if host not in VULNERABILITIES:
        print("No known vulnerabilities.")
        return

    vuln = VULNERABILITIES[host].get(cve)

    if vuln is None:
        print("CVE not found.")
        return

    print("[*] Target:", host)
    print("[*] Vulnerability:", vuln["name"])
    print("[*] Severity:", vuln["severity"])

    pause()
    print("[*] Checking vulnerability...")
    pause()

    if vuln["vulnerable"]:
        print("[+] Vulnerability confirmed!")
        pause()
        print("[+] Simulated exploit successful!")
        print("[+] Lab access granted.")

        global current_host
        current_host = host
    else:
        print("[-] Target is patched.")


def ping(target):
    ip = resolve_host(target)

    if ip is None:
        print("Unknown host.")
        return

    print("PING " + ip)

    for i in range(4):
        pause()
        print(
            "64 bytes from " + ip +
            ": time=" + str(random.randint(2, 40)) + " ms"
        )


def traceroute(target):
    ip = resolve_host(target)

    if ip is None:
        print("Unknown host.")
        return

    print("Traceroute to " + ip)

    for i in range(1, 4):
        pause()
        print(
            str(i) + " 192.168.56." +
            str(random.randint(1, 254))
        )

    print("Destination reached.")


def filesystem(command):
    global current_dir

    if command == "pwd":
        print(current_dir)

    elif command == "ls":
        print("  ".join(FILES.get(current_dir, [])))

    elif command.startswith("cd "):
        target = command[3:].strip()

        if target == "..":
            current_dir = current_dir.rsplit("/", 1)[0] or "/"

        elif target == "/":
            current_dir = "/"

        else:
            path = current_dir.rstrip("/") + "/" + target

            if path in FILES:
                current_dir = path
            else:
                print("Directory not found.")

    elif command.startswith("cat "):
        name = command[4:].strip()
        path = current_dir.rstrip("/") + "/" + name

        print(CONTENTS.get(path, "File not found."))

    elif command.startswith("grep "):
        parts = command.split(" ", 2)

        if len(parts) < 3:
            print("Usage: grep TEXT FILE")
            return

        word, name = parts[1], parts[2]
        path = current_dir.rstrip("/") + "/" + name

        for line in CONTENTS.get(path, "").split("\n"):
            if word in line:
                print(line)


def help_menu():
    print("""
NETWORK:
  nmap HOST
  nmap -sV HOST
  ping HOST
  traceroute HOST

REMOTE:
  ssh HOST

EXPLOITATION:
  exploit HOST CVE

FILES:
  ls
  cd DIR
  pwd
  cat FILE
  grep TEXT FILE

SYSTEM:
  whoami
  uname
  ip addr
  ip route
  history
  logs
  status

OTHER:
  clear
  help
  exit
""")


def execute(command):
    if not command:
        return True

    history.append(command)

    if command == "help":
        help_menu()

    elif command == "exit":
        return False

    elif command == "clear":
        print("\n" * 25)

    elif command.startswith("nmap -sV "):
        scan(command[9:].strip(), True)

    elif command.startswith("nmap "):
        scan(command[5:].strip())

    elif command.startswith("ping "):
        ping(command[5:].strip())

    elif command.startswith("traceroute "):
        traceroute(command[11:].strip())

    elif command.startswith("ssh "):
        ssh(command[4:].strip())

    elif command.startswith("exploit "):
        parts = command.split()

        if len(parts) == 3:
            exploit(parts[1], parts[2])
        else:
            print("Usage: exploit HOST CVE")

    elif command in ("ls", "pwd") or command.startswith(
        ("cd ", "cat ", "grep ")
    ):
        filesystem(command)

    elif command == "whoami":
        print("root" if current_host != "localhost" else "user")

    elif command == "uname":
        print("IRONCLAD-Linux 6.1.0 simulated")

    elif command == "ip addr":
        print("eth0: 192.168.56.100/24")
        print("lo: 127.0.0.1")

    elif command == "ip route":
        print("default via 192.168.56.1 dev eth0")

    elif command == "history":
        for i, item in enumerate(history):
            print(str(i + 1) + "  " + item)

    elif command == "logs":
        print(CONTENTS["/var/log/auth.log"])
        print(CONTENTS["/var/log/system.log"])

    elif command == "status":
        print("Current host:", current_host)
        print("Network: simulated")
        print("Hosts:", len(HOSTS))

    else:
        print("Command not found:", command)

    return True


def main():
    banner()

    while True:
        try:
            command = input(current_host + ":" + current_dir + "$ ")

            if execute(command) is False:
                print("Exiting IRONCLAD.")
                break

        except KeyboardInterrupt:
            print("\nInterrupted.")

        except Exception as error:
            print("Error:", error)


main()

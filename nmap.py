import socket
import select

target = input("Cíl: ")
ports = int(input("Range: ")) + 1

for port in range(ports):
    s = socket.socket()
    s.setblocking(False)

    try:
        s.connect((target, port))
    except OSError:
        pass

    poll = select.poll()
    poll.register(s, select.POLLOUT)

    events = poll.poll(100)

    if events:
        err = s.getsockopt(socket.SOL_SOCKET, socket.SO_ERROR)

        if err == 0:
            print(f"[OPEN] {port}")
        else:
            print(f"[CLOSED] {port}")
    else:
        print(f"[TIMEOUT] {port}")

    poll.unregister(s)
    s.close()

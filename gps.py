from machine import UART, Pin
import time

gps = UART(
    1,
    baudrate=9600,
    tx=Pin(43),
    rx=Pin(44)
)

while True:
    if gps.any():
        data = gps.readline()

        if data:
            print(data.decode().strip())

    time.sleep(0.1)
  

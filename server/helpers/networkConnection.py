import network
import machine
import socket
import time
import struct
from machine import Pin
from server import secrets


print("Starting the network...")

host = "pool.ntp.org"
NTP_DELTA = 2208988800



def setTime():
    NTP_QUERY = bytearray(48)
    NTP_QUERY[0] = 0x1B
    addr = socket.getaddrinfo(host, 123)[0][-1]
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.settimeout(1)
        res = s.sendto(NTP_QUERY, addr)
        msg = s.recv(48)
    finally:
        s.close()
    val = struct.unpack("!I", msg[40:44])[0]
    t = val - NTP_DELTA    
    tm = time.gmtime(t)
    machine.RTC().datetime((tm[0], tm[1], tm[2], tm[6] + 1, tm[3], tm[4], tm[5], 0))

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(secrets.SSID,secrets.NETPASS)


# wait for connect
max_wait = 10
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        print("wlan status is less than 0 or greater 3")
        break
    max_wait -= 1
    print('waiting for connection...')
    time.sleep(1)

if wlan.status() !=3:
    raise RuntimeError("Network connection failed")
else:
    print("connected")
    status = wlan.ifconfig()
    print('ip = ' + status[0])


setTime()
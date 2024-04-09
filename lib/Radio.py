# LunarX Bot Radio Controller
# Yu Hin Hau
# billwaahau@gmail.com
# April 9, 2024

import wifi
import ipaddress
import socketpool
import select
import time

class Radio:

    def __init__(self, ssid, password, ipAddress = "192.168.1.138", port = 8888, ap_mode = True):

        self.commandDict = {}

        self.ssid = ssid
        self.password = password
        self.ipAddress = ipAddress
        self.port = port

        self.ipv4 =  ipaddress.IPv4Address(self.ipAddress)
        self.netmask =  ipaddress.IPv4Address("255.255.255.0")
        self.gateway =  ipaddress.IPv4Address("192.168.1.0")

        if wifi.radio.ap_active:
            wifi.radio.stop_ap()

        if (ap_mode):
            self.radioStartAP()
        else:
            self.radioConnect()

        self.socket.setblocking(False)
        self.t_heartBeat = time.monotonic()


    # Bind External Methods to Dictionary
    def bindCommand(self, key, command):
        self.commandDict[key] = command



    def radioConnect(self):
        wifi.radio.set_ipv4_address(ipv4=self.ipv4, netmask=self.netmask, gateway=self.gateway)
        wifi.radio.connect(ssid=self.ssid, password=self.password)
        sp = socketpool.SocketPool(wifi.radio)
        self.socket = sp.socket(sp.AF_INET, sp.SOCK_DGRAM) # UDP
        self.socket.bind((str(wifi.radio.ipv4_address), self.port)) # Connected Wifi

        print("Connected to SSID: {}, password: {}".format(self.ssid, self.password))
        print("IP address: ", wifi.radio.ipv4_address)
        print("Port: ", self.port)

    def radioStartAP(self):
        wifi.radio.set_ipv4_address_ap(ipv4=self.ipv4, netmask=self.netmask, gateway=self.gateway)
        wifi.radio.start_ap(ssid=self.ssid, password=self.password)
        sp = socketpool.SocketPool(wifi.radio)
        self.socket = sp.socket(sp.AF_INET, sp.SOCK_DGRAM) # UDP
        self.socket.bind((str(wifi.radio.ipv4_address_ap), self.port)) # Access Point

        print("Access point created with SSID: {}, password: {}".format(self.ssid, self.password))
        print("IP address: ", wifi.radio.ipv4_address_ap)
        print("Port: ", self.port)

    def processSignal(self, ip_dest = "192.168.1.141", port_dest = 56790):
        self.heartBeat(ip_dest, port_dest)


    def heartBeat(self, ip_dest = "192.168.1.141", port_dest = 56790):

        inputs = [self.socket]
        outputs = [self.socket]

        readable, writable, exceptional = select.select(inputs, outputs, inputs, 0.1)

        for s in writable:
            if (time.monotonic() - self.t_heartBeat > 2):
                try:
                    cmd = f"=HeartBeat:{time.monotonic():.1f}="
                    s.sendto(bytes(cmd, 'utf-8'), (ip_dest, port_dest))
                    print(f"[TX @ {time.monotonic()}] {cmd}")
                except Exception as e:
                    print(f"[ERROR @ {time.monotonic()}] Desktop Client Not Connected!")

                self.t_heartBeat = time.monotonic()

        for s in readable:
                message = bytearray(32)
                s.recv_into(message)
                message = str(message, 'utf-8')
                print(f"[RX @ {time.monotonic()}] {message}")
                payload = message.split('=')[1]

                cmd = None
                arg = None
                tmp = payload.split(':')

                if(len(tmp)==2):
                    cmd = tmp[0]
                    arg = tmp[1]
                else:
                    cmd = tmp[0]

                print(f"[INFO @ {time.monotonic()}] CMD: [{cmd}] ARG: [{arg}]")

                # Call Binded External Commands with Argument Handling
                if cmd in self.commandDict:
                    funct = self.commandDict[cmd]

                    if arg is None:
                        funct()
                    else:
                        funct(arg)




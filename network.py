import socket
from time import time, sleep
from struct import unpack
from .packet import *
from .bulb import Bulb
from .connection import Connection


class Network:
    port = 56700
    ip = ''
    broadcast_ip = '255.255.255.255'
    gateway_mac = bytearray(6)
    all_bulbs_mac = bytearray(6)
    receive_size = 2048
    recv_timeout = 2
    search_timeout = 2
    bulbs = set()
    connection = None

    def __init__(self):
        self.connection = Connection()
        self.bulbs = set()

    def search(self):
        for i in range(2):
            self.connection.send(self.all_bulbs_mac, self.gateway_mac, PacketType.GET_PAN_GATEWAY, 1, None)

        sleep(0.5)
        start_time = time()
        while True:
            try:
                self.connection.socket.settimeout(self.recv_timeout)
                data, address = self.connection.socket.recvfrom(self.receive_size)
                packet = Packet.FromBulb(data)
                if packet is not None:
                    header, payload = packet.get_data()
                    if header.code is PacketType.PAN_GATEWAY.code:
                        print "Found: " + address[0] + "  MAC: " + "%x:%x:%x:%x:%x:%x" % unpack("BBBBBB", header.target)
                        self.bulbs.add(Bulb(ip=address[0], site=header.site, mac=header.target, connection=self.connection))
            except socket.timeout:
                pass

            if time() > (self.search_timeout + start_time):
                break

    def get_lights_by_tags(self, tag):
        for bulb in self.bulbs:
            if bulb.get_tags() == label:
                return bulb
        return None

    def get_light_by_label(self, label):
        for bulb in self.bulbs:
            if bulb.get_label() == label:
                return bulb
        return None

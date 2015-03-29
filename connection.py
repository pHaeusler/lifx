import socket
import struct
import select
import time
import errno
from socket import error as socket_error
from .packet import *

class Connection:
    port = 56700
    broadcast_ip = '255.255.255.255'
    bind_ip = ''
    receive_size = 2048

    def __init__(self, connect=True):
        if connect:
            self.connect()

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.socket.bind((self.bind_ip, self.port))

    def disconnect(self):
        if self.socket is not None:
            self.socket.close()
            self.socket = None

    def send(self, mac, site, packet_type, ack, *data):
        packet = Packet.ToBulb(packet_type, mac, site, ack, *data).get_bytes()
        self.socket.sendto(packet, (self.broadcast_ip, self.port))

    def receive(self, timeout=1):
        ready = select.select([self.socket], [], [], timeout)
        if ready[0]:
            data = self.socket.recv(self.receive_size)
            return Packet.FromBulb(data)
        return None

    def listen_for_packet(self, packet_filter, num_packets=1, timeout=2):
        start_time = time.time()
        packets = []
        while True:
            packet = self.receive()
            if packet is not None and (packet.packet_type.code is packet_filter.code or (isinstance(packet_filter, list) and packet.packet_type.code in packet_filter)):
                if num_packets == 1:
                    return packet
                else:
                    packets.append(packet)
            if timeout is not None and time.time() > start_time + timeout:
                break
        if num_packets == 1:
            return None
        return packets

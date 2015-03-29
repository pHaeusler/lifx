from .enums import *
from .packet import *
from .connection import Connection


class Bulb:
    max_retries = 5

    def __init__(self, ip, site, mac, connection):
        self.ip = ip
        self.site = site
        self.mac = mac
        self.connection = connection

    def __hash__(self):
        return hash((self.ip, self.site, self.mac))

    def __eq__(self, other):
        return (self.ip, self.site, self.mac) == (other.ip, other.site, other.mac)

    def send(self, packet_type, ack=0, *data):
        self.connection.send(self.mac, self.site, packet_type, ack, *data)

    def retry(self, packet_type_send, packet_type_reply, *data):
        retries = 0
        while True:
            self.send(packet_type_send, 1, *data)
            packet = self.connection.listen_for_packet(packet_type_reply)
            if packet is not None:
                return packet
            retries += 1
            if retries > self.max_retries:
                print "Bulb did not respond"
                return None

    def on(self):
        packet = self.retry(PacketType.SET_POWER_STATE, PacketType.POWER_STATE, Power.ON)
        if packet is not None:
            header, payload = packet.get_data()
            if payload is not None:
                return bool(payload.onoff)
        else:
            return None

    def off(self):
        packet = self.retry(PacketType.SET_POWER_STATE, PacketType.POWER_STATE, Power.OFF)
        if packet is not None:
            header, payload = packet.get_data()
            if payload is not None:
                return bool(payload.onoff)
        else:
            return None

    def is_on(self):
        packet = self.retry(PacketType.GET_POWER_STATE, PacketType.POWER_STATE)
        if packet is not None:
            header, payload = packet.get_data()
            if payload is not None:
                return bool(payload.onoff)
        else:
            return None

    def get_label(self):
        packet = self.retry(PacketType.GET_BULB_LABEL, PacketType.BULB_LABEL)
        if packet is not None:
            header, payload = packet.get_data()
            if payload is not None:
                return payload.label.replace('\x00', '')
        else:
            return None

    def set_label(self, label):
        packet = self.retry(PacketType.SET_BULB_LABEL, PacketType.BULB_LABEL, label)
        if packet is not None:
            header, payload = packet.get_data()
            if payload is not None:
                return payload.label.replace('\x00', '')
        else:
            return None

    def get_tags(self):
        packet = self.retry(PacketType.GET_TAGS, PacketType.TAGS)
        if packet is not None:
            header, payload = packet.get_data()
            if payload is not None:
                return payload.tags
        else:
            return None

    def set_brightness(self, brightness, duration, relative=False):
        if relative:
            packet = self.retry(PacketType.SET_DIM_RELATIVE, PacketType.LIGHT_STATUS)
        else:
            packet = self.retry(PacketType.SET_DIM_ABSOLUTE, PacketType.LIGHT_STATUS)
        if packet is not None:
            header, payload = packet.get_data()
            if payload is not None:
                return payload
        else:
            return None

    def get_light_state(self):
        packet = self.retry(PacketType.GET_LIGHT_STATE, PacketType.LIGHT_STATUS)
        if packet is not None:
            header, payload = packet.get_data()
            if payload is not None:
                return payload
        else:
            return None

    def set_light_state(self, stream, hue, saturation, brightness, kelvin, duration):
        packet = self.retry(PacketType.SET_LIGHT_COLOUR, 
                            PacketType.LIGHT_STATUS, stream,
                            hue,
                            saturation,
                            brightness,
                            kelvin,
                            duration)
        if packet is not None:
            header, payload = packet.get_data()
            if payload is not None:
                return payload
        else:
            return None

    def get_temperature(self):
        packet = self.retry(PacketType.GET_TEMPERATURE, PacketType.TEMPERATURE)
        if packet is not None:
            header, payload = packet.get_data()
            if payload is not None:
                return payload.temperature
        else:
            return None

    def reboot():
        self.send(PacketType.REBOOT)

    def get_info(self):
        packet = self.retry(PacketType.GET_INFO, PacketType.INFO)
        if packet is not None:
            header, payload = packet.get_data()
            if payload is not None:
                return payload
        else:
            return None

    def get_version(self):
        packet = self.retry(PacketType.GET_VERSION, PacketType.VERSION_STATE)
        if packet is not None:
            header, payload = packet.get_data()
            if payload is not None:
                return payload
        else:
            return None

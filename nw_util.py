import subprocess
import re
import fcntl, socket, struct


def get_wireless_interfaces():
    output = subprocess.check_output("iwconfig", shell=True, stderr=subprocess.DEVNULL).decode("utf-8")
    pattern = re.compile(r'^.+?\b')
    return pattern.findall(output)


def get_hw_addr(if_name):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    info = fcntl.ioctl(s.fileno(), 0x8927, struct.pack('256s', if_name[:15].encode()))
    return info[18:24]


def get_pseudo_unique_ip(if_name):
    mac = get_hw_addr(if_name)
    last_3_octets_as_num = struct.unpack(">L", b"\x00" + mac[-3:])[0] + (10 << 24)
    return socket.inet_ntoa(struct.pack("!L", last_3_octets_as_num))

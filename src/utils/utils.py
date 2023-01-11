import logging
import ipaddress


def set_logger():
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    log = logging.getLogger('kademlia')
    log.addHandler(handler)
    log.setLevel(logging.DEBUG)


def valid_ip(ip : str):
    try:
        ipaddress.ip_address(ip)
    except ValueError:
        print("ERROR: invalid ip address")
        exit()


def valid_port(port : int):
    if port < 1 or port > 65535:
        print("ERROR: invalid port")
        exit()

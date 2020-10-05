#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""A low-level utility that returns the local IP address in use.
"""

import socket


def get_private_ip():
    """Return dotted quad IP address in use.
    """
    testing_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable for a meaningful result.
        testing_socket.connect(('10.255.255.255', 1))
        IP = testing_socket.getsockname()[0]
    except Exception:
        # no ethernet IP address was found. Return localhost.
        IP = '127.0.0.1'
    finally:
        testing_socket.close()
    return IP

if __name__ == "__main__":
    print(get_private_ip())


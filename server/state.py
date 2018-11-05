#!/usr/bin/env python3

from typing import List, Dict
import json
import ipaddress


class State:
    def __init__(self, config: str, mode: str):
        self.config_fname = config
        self.mode = mode
        self.config = None
        self.read_config()

    def get_config(self, ip: str):
        ip = ipaddress.ip_address(ip)

        if self.config is None:
            raise Exception("Config is None")

        if "any" in self.config[self.mode]:
            return json.dumps(self.config[self.mode]["any"])

        for subnet in self.config[self.mode]:
            if ip in ipaddress.ip_network(subnet):
                return json.dumps(self.config[self.mode][subnet])
        return "IP address isn't in any subnet"

    def read_config(self):
        with open(self.config_fname) as f:
            data = json.load(f)

            # Sanity check, ipaddress.ip_network throws a ValueError if any subnet is invalid
            for mode in data:
                if "any" not in data[mode]:
                    for subnet in data[mode]:
                        ipaddress.ip_network(subnet)
            self.config = data

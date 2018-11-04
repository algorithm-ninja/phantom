#!/usr/bin/env python3

from typing import List, Dict
import json
import ipaddress

class State:
    def __init__(self, config: str, default_mode: str):
        self.config_fname = config
        self.default_mode = default_mode
        self.known_ips: List[ipaddress.IPv6Address] = list()
        self.mode: Dict[ipaddress.IPv6Address, str] = dict()
        self.config = None
        self.read_config()

    def get_config(self, ip: str):
        self.read_ethers()
        ip = ipaddress.ip_address(ip)

        if self.config is None: raise Exception("Config is None")
        if ip not in self.mode:
            self.mode[ip] = "wait"
            print("WARN: ip " + str(ip) + " is unknown")
        mode = self.mode[ip]

        if "any" in self.config[mode]:
            return json.dumps(self.config[mode]["any"])

        for subnet in self.config[mode]:
            if ip in ipaddress.ip_network(subnet):
                return json.dumps(self.config[mode][subnet])
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
    
    def read_ethers(self):
        self.known_ips.clear()
        with open("/etc/dnsmasq.d/ethers.conf", "r") as fin:
            for line in fin.readlines():
                line = line.strip()
                if len(line) == 0: continue
                if len(line.split('[')) != 2:
                    raise Exception("Malformed ethers file")
                if len(line.split('[')[1].split(']')) != 2:
                    raise Exception("Malformed ethers file")
                
                ip = ipaddress.ip_address(line.split('[')[1].split(']')[0])
                self.known_ips.append(ip)
                if ip not in self.mode:
                    self.mode[ip] = self.default_mode


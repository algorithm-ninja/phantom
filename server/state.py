#!/usr/bin/env python3

from typing import List, Dict
import json

class State:
    def __init__(self, config: str, default_mode: str):
        self.config_fname = config
        self.known_ips: List[str] = list()
        self.mode: Dict[str, str] = dict()

        with open("/etc/ethers", "r") as fin:
            for line in fin.readlines():
                line = line.strip()
                if len(line) == 0: continue
                if len(line.split(' ')) != 2:
                    raise Exception("Malformed ethers file")
                ip = line.split(' ')[1]
                self.known_ips.append(ip)
                self.mode[ip] = default_mode

        self.config = None
        self.read_config()

    def get_config(self, ip: str):
        if self.config is None: raise Exception("Config is None")
        if ip not in self.mode:
            self.mode[ip] = "wait"
            print("WARN: ip " + ip + " is unknown")
        mode = self.mode[ip]

        if "any" in self.config[mode]:
            return json.dumps(self.config[mode]["any"])
        elif self.is_worker(ip):
            return json.dumps(self.config[mode]["worker"])
        else:
            return json.dumps(self.config[mode]["contestant"])
    
    def is_worker(self, ip: str):
        return ip.startswith("fdfd:d")
    
    def read_config(self):
        with open(self.config_fname) as f:
            data = json.load(f)

            # Sanity check
            for mode in data:
                if "contestant" not in data[mode] or "worker" not in data[mode]:
                    if "any" not in data[mode]:
                        raise Exception("Malformed config file: missing 'contestant', 'worker' or 'any'")

            self.config = data

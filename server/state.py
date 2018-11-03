#!/usr/bin/env python3

from typing import List, Dict
from json import json

class State:
    def __init__(self, config: str):
        self.known_ips: List[str] = list()
        self.mode: Dict[str, str] = dict()
        self.config = None
        self.read_config()

    def get_config(self, ip: str):
        if self.config is None: raise Exception("Config is None")
        if ip not in self.mode: raise Exception("Requested ip unknown")
        mode = self.mode[ip]

        if "any" in self.config[mode]:
            return self.config[mode]["any"]
        elif is_worker(ip):
            return self.config[mode]["worker"]
        else:
            return self.config[mode]["contestant"]
    
    def is_worker(self, ip: str):
        return ip.startswith("fdfd:d")
    
    def read_config(self):
        with open("config.json") as f:
            data = json.load(f)

            # Sanity check
            for mode in data:
                if "contestant" not in data[mode] or "worker" not in data[mode]:
                    if "any" not in data[mode]:
                        raise Exception("Malformed config file: missing 'contestant', 'worker' or 'any'")

            self.config = d

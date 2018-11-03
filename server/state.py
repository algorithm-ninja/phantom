#!/usr/bin/env python3

from typing import List, Dict
from json import json

class State:
    def __init__(self, config: str):
        self.known_ips: List[str] = list()
        self.mode: Dict[str, str] = dict()
        self.read_config()

    def get_config(self, ip: str):
        raise NotImplementedError()
    
    def read_config(self):
        with open('config.json') as f:
            data = json.load(f)

            # Sanity check
            for mode in data:
                if 'contestant' not in data[mode] or 'worker' not in data[mode]:
                    if 'any' not in data[mode]:
                        raise Exception('Malformed config file')

            self.config = d

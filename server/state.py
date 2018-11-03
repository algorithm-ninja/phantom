from typing import List, Dict


class State:
    def __init__(self, config: str):
        self.known_ips: List[str] = list()
        self.mode: Dict[str, str] = dict()
        # TODO read config file

    def get_config(self, ip: str):
        raise NotImplementedError()

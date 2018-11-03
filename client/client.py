#!/usr/bin/env python3

import json
import requests
import subprocess
import sys
import time

PREFIX = "fdcd::"
GATEWAY = f"[{PREFIX}1]:5000"
CONFIG_URL = f"http://{GATEWAY}/config?ip="


def my_ip():
    proc = subprocess.run(
        f"ip --json addr show to {PREFIX}/24", stdout=subprocess.PIPE, shell=True)
    ips = json.loads(proc.stdout)
    if len(ips) != 1:
        print("[E] Found zero or more than one possible interface!")
        print(json.dumps(ips, indent=4))
        sys.exit(1)
    device = ips[0]["ifname"]
    print(f"[*] The network device is {device}")
    possilbe_ips = list(filter(
        bool, map(lambda x: x.get("local"), ips[0]["addr_info"])))
    if len(possilbe_ips) != 1:
        print("[E] Found zero or more than one possible ips!")
        print(f"    Possible ips: {possilbe_ips}")
        print(json.dumps(ips, indent=4))
        sys.exit(1)
    return possilbe_ips[0]


def exec_command(cmd):
    print(f"[*] exec: {cmd}")
    proc = subprocess.run(cmd, shell=True)
    return proc.returncode


def run_commands(cmds):
    for cmd in cmds:
        code = exec_command(cmd)
        if code:
            sys.exit(code)


def wait_mode(config):
    run_commands(config["cmds"])
    print("[*] Done! I'll wait here :P")
    while True:
        time.sleep(1)


def exec_mode(config):
    run_commands(config["cmds"])
    print("[W] I should not be here! OS hasn't booted :c")
    sys.exit(2)


def main():
    print("Welcome in phantom!")
    url = CONFIG_URL + my_ip()
    print(f"[*] Config url: {url}")

    response = requests.get(url)
    print(
        f"[*] Response status is {response.status_code} ({len(response.content)} B)")

    config = json.loads(response.content)
    print(f"[*] The config is:")
    print(json.dumps(config, indent=4))

    mode = config["mode"]
    print(f"[*] Running in mode {mode}")
    if mode == "wait":
        wait_mode(config)
    elif mode == "exec":
        exec_mode(config)
    else:
        print(f"[X] Unknown mode {mode}, it's not wait nor exec")
        return 1


if __name__ == "__main__":
    sys.exit(main())

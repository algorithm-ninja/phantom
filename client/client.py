#!/usr/bin/env python3

import json
import requests
import subprocess
import sys
import time
import os

PREFIX = "fdcd::"
GATEWAY = f"[{PREFIX}1]"
SERVER_PREFIX = f"http://{GATEWAY}:5000"
CONFIG_URL = f"{SERVER_PREFIX}/config?ip="


def my_ip():
    wired, wireless, device = None, None, ""

    print("[*] Waiting for a network interface")
    wait_start = time.time()
    while True:
        proc = subprocess.run(
            f"ip --json addr show to {PREFIX}/24", stdout=subprocess.PIPE, shell=True)
        ips = json.loads(proc.stdout)

        wired, wireless, bond = None, None, None
        for interface in ips:
            if interface["operstate"] != "UP":
                continue
            if interface["ifname"].startswith("e"):
                wired = interface
            elif interface["ifname"].startswith("w"):
                wireless = interface
            elif interface["ifname"].startswith("bond"):
                bond = interface

        if bond is not None:
            print("[*] Bonding interface found")
            device = bond["ifname"]
            break
        if wired is not None:
            print("[*] Wired interface found")
            device = wired["ifname"]
            break
        if (time.time() - wait_start) > 20:
            if wireless is not None:
                print("[*] Wireless interface found")
                device = wireless["ifname"]
                break

        time.sleep(1)

    print(f"[*] The network device is {device}")
    possible_ips = list(filter(
        bool, map(lambda x: x.get("local"), ips[0]["addr_info"])))
    if len(possible_ips) != 1:
        print("[E] Found zero or more than one possible ips!")
        print(f"    Possible ips: {possible_ips}")
        print(json.dumps(ips))

        subprocess.run(f'ip addr flush dev {device}', shell=True)
        print("[E] Rebooting in 10 seconds")
        time.sleep(10)
        subprocess.run('reboot', shell=True)

    ip = possible_ips[0]
    os.environ["NETWORK_DEVICE"] = device
    os.environ["MY_IP"] = ip

    data = json.loads(subprocess.run(
        f"ip --json addr show dev {device}", shell=True, stdout=subprocess.PIPE).stdout)
    dev_info = next(x for x in data if x.get("ifname") == device)
    os.environ["MY_MAC"] = dev_info.get("address")

    print(f"[*] My IP is {ip}")

    return ip


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


def check_update():
    print("[*] Checking for updates")
    response = requests.get(f"{SERVER_PREFIX}/client_hash")
    with open("/root/client.py.hash", "wb") as f:
        f.write(response.content)
    proc = subprocess.run("b2sum -c client.py.hash", shell=True, cwd="/root")
    if proc.returncode == 0:
        print("[*] Alredy up-to-date")
    else:
        print("[*] Updated needed")
        response = requests.get(f"http://{GATEWAY}/static/client.py")
        with open("/root/client.py", "wb") as f:
            f.write(response.content)
        print("[*] Updated successfully")
        time.sleep(5)
        subprocess.run("reboot", shell=True)


def main():
    print("Welcome in phantom!")
    url = CONFIG_URL + my_ip()
    check_update()
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

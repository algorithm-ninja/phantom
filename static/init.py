#!/usr/bin/env python3

from subprocess import run, PIPE
import requests
import os, time

SERVER_IP = "[fdcd::1]"
mac = os.environ['MY_MAC']
ip = ''

def ask_integer(desc, start, end, h, w):
    res = ''
    cmd = f"dialog --nocancel --inputbox \"{desc} [{start}-{end}]:\" {h} {w}"
    
    while res == '':
        res = run(cmd, shell=True, stderr=PIPE).stderr.decode()
        try:
            assert(start <= int(res) <= end)
        except:
            run("dialog --msgbox \"Not a valid integer\" 5 23", shell=True)
            res = ''

    return int(res)

if run("dialog --defaultno --yesno \"Am I a worker?\" 5 19", shell=True, stderr=PIPE).returncode != 0:
    while True:
        row = ask_integer("Enter row", 1, 65535, 8, 25)
        col = ask_integer("Enter column", 1, 65535, 8, 28)

        row = hex(row)[2:]
        col = hex(col)[2:]
        
        url = "http://" + SERVER_IP + "/collector/contestant?mac=" + mac + "&row=" + row + "&col=" + col
        r = requests.get(url)
        if r.status_code != 200:
            run(f"dialog --msgbox \"Error: {r.text}\" 6 40", shell=True)
        else:
            ip = r.text
            print(ip)
            break
else:
    while True:
        num = ask_integer("Enter number", 1, 65535, 8, 28)

        num = hex(num)[2:]

        url = "http://" + SERVER_IP + "/collector/worker?mac=" + mac + "&num=" + num
        r = requests.get(url)
        if r.status_code != 200:
            run(f"dialog --msgbox \"Error: {r.text}\" 6 40", shell=True)
        else:
            ip = r.text
            print(ip)
            break

run("dialog --infobox \"Done, waiting to reboot\nI am " + ip + "\" 4 27", shell=True)

ts = ''
r = requests.get("http://" + SERVER_IP + "/collector/reboot_timestamp")
if r.status_code != 200:
    run("reboot", shell=True)
else:
    ts = r.text

while True:
    r = requests.get("http://" + SERVER_IP + "/collector/reboot_timestamp")
    if r.status_code != 200 or ts != r.text:
        run("reboot", shell=True)
    ts = r.text
    time.sleep(1)


#!/usr/bin/env python3

from state import State
from flask import Flask, request
import argparse
import subprocess
import os.path

app = Flask(__name__)


@app.route("/config", methods=["GET"])
def config():
    ip = request.args.get("ip")
    if ip is None:
        return "Missing parameter 'ip'"
    return state.get_config(ip.lower())


@app.route("/client_hash", methods=["GET"])
def client_hash():
    path = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), "../static")
    return subprocess.run(f"b2sum client.py", shell=True, cwd=path, stdout=subprocess.PIPE).stdout


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config.json",
                        help="Configuration file, defaults to config.json")
    parser.add_argument("--host", default="::", help="Host to listen on")
    parser.add_argument("--mode", default="default",
                        help="mode for computers")
    args = parser.parse_args()

    state = State(args.config, args.mode)
    app.run(threaded=True, host=args.host)

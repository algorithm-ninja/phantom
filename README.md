# Phantom

## Server

`./server.py`

Example config file: `server/config.json`

Mode:

```
exec: just execute
wait: execute and wait
```

## How to run

### On the server container:

These must all be running:

`dnsmasq.service`, `rsyncd.service`, `phantom-server`, `phantom-collector`

To clear all IP-MAC associations:

`echo | sudo tee /etc/dnsmasq.d/ethers.conf`

`sudo systemctl restart phantom-collector`

`sudo systemctl restart dnsmasq.service`

### On the PCs

Select if worker or contestant

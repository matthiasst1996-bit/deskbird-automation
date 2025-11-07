#!/bin/bash

# Starte OpenVPN im Hintergrund
openvpn --config /etc/openvpn/proton/de-zurich-01.protonvpn.com.udp.ovpn --daemon --log /tmp/vpn.log

# Warte bis VPN verbunden ist
sleep 10

# Führe Skripte aus
python run_scripts.py

# Stoppe VPN am Ende
pkill -f openvpn

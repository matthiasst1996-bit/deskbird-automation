FROM python:3.11-slim

# Installiere OpenVPN und andere Dependencies
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    openvpn \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Lade ProtonVPN OpenVPN config
RUN mkdir -p /etc/openvpn/proton && \
    cd /etc/openvpn/proton && \
    wget -q https://api.protonvpn.ch/downloads/linux/OpenVPN/de/ProtonVPN_de.zip && \
    unzip -q ProtonVPN_de.zip && \
    rm ProtonVPN_de.zip

# Installiere webdriver-manager
RUN pip install webdriver-manager

# Kopiere requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopiere Skripte
COPY Arbeitsplatz-deskbird_login.py .
COPY Parkplatz-deskbird_login.py .
COPY run_scripts.py .

# VPN-Start-Script
COPY start_vpn.sh .
RUN chmod +x start_vpn.sh

# Starte VPN dann Skripte
CMD ["./start_vpn.sh"]

FROM python:3.11-slim

# Installiere Chrome und notwendige Abhängigkeiten
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Installiere Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' && \
    apt-get update && \
    apt-get install -y google-chrome-stable \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Installiere ChromeDriver (verwende webdriver-manager statt manuellem Download)
RUN pip install webdriver-manager

# Installiere Python-Abhängigkeiten
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopiere deine Skripte
COPY Arbeitsplatz-deskbird_login.py .
COPY Parkplatz-deskbird_login.py .
COPY run_scripts.py .

# Starte die Skripte
CMD ["python", "run_scripts.py"]

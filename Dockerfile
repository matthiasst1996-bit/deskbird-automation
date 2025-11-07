FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    wget curl gnupg unzip \
    && rm -rf /var/lib/apt/lists/*

RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 78BD65473CB3BD13 && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable && \
    rm -rf /var/lib/apt/lists/*

RUN pip install webdriver-manager

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY Arbeitsplatz-deskbird_login.py .
COPY Parkplatz-deskbird_login.py .
COPY run_scripts.py .

CMD ["python", "run_scripts.py"]

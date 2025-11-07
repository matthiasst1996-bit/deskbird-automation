FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

RUN pip install webdriver-manager

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY Arbeitsplatz-deskbird_login.py .
COPY Parkplatz-deskbird_login.py .
COPY run_scripts.py .

CMD ["python", "run_scripts.py"]

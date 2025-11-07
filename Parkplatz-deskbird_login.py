from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")

driver = webdriver.Chrome(
    service=Service('/usr/bin/chromedriver'),
    options=chrome_options
)

USERNAME = ""
PASSWORD = ""

BASE_URL = "https://app.deskbird.com"

def main():
    try:
        driver.get(BASE_URL + "/login")
        time.sleep(3)
        
        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "email"))
        )
        username_field.send_keys(USERNAME)
        
        password_field = driver.find_element(By.ID, "password")
        password_field.send_keys(PASSWORD)
        password_field.send_keys(Keys.RETURN)
        
        time.sleep(5)
        
        WebDriverWait(driver, 10).until(
            EC.url_changes(BASE_URL + "/login")
        )
        
        print("Login erfolgreich für Parkplatz!")
        
        time.sleep(2)
        
    except Exception as e:
        print(f"Fehler bei Parkplatz-Login: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()

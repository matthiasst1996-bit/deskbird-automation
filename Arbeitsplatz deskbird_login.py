import time
import random
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def human_typing(element, text):
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.1, 0.3))

def human_click(driver, element):
    actions = ActionChains(driver)
    actions.move_to_element(element).pause(random.uniform(0.4, 0.8)).click().perform()

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")

chrome_options.add_argument("start-maximized")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=chrome_options
)


try:
    driver.get("https://app.deskbird.com/login/check-in")

    email_input = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.NAME, "email"))
    )
    human_typing(email_input, "Strotmann.M@proservicekoeln.de")
    time.sleep(random.uniform(1.5, 3.0))

    def wait_for_enabled_signin(driver):
        btn = driver.find_element(By.CSS_SELECTOR, "button.p-element.p-ripple.font-ProximaNovaBold.w-full.p-button.p-component")
        return btn if btn.is_enabled() else False
    
    sign_in_btn = WebDriverWait(driver, 30).until(wait_for_enabled_signin)
    human_click(driver, sign_in_btn)
    time.sleep(random.uniform(2.0, 3.5))

    sign_in_email_btn = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//button[.//span[contains(text(),'Sign in with email')]]"))
    )
    human_click(driver, sign_in_email_btn)
    time.sleep(random.uniform(2.0, 3.5))

    password_input = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.NAME, "password"))
    )
    human_typing(password_input, "Erfolg2024!")
    time.sleep(random.uniform(1.5, 3.0))

    confirm_btn = WebDriverWait(driver, 40).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.p-element.p-ripple.font-ProximaNovaBold.w-full.p-button.p-component[type='submit']"))
    )
    time.sleep(random.uniform(1.0, 2.0))
    human_click(driver, confirm_btn)

    print("Login erfolgreich abgeschlossen!")
    time.sleep(5)

    target_date = datetime.now() + timedelta(days=14)
    target_day = target_date.day
    target_month = target_date.strftime("%b")
    target_date_text = f"{target_day} {target_month}"
    print(f"Suche nach Zieldatum: {target_date_text}")

    viewport = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "cdk-virtual-scroll-viewport"))
    )
    
    found_target_date = False
    for i in range(30):
        try:
            target_header = driver.find_element(By.XPATH, f"//*[contains(text(), '{target_date_text}')]")
            print(f"Zieldatum gefunden: {target_date_text}")
            found_target_date = True
            time.sleep(1)
            break
        except:
            pass
        
        driver.execute_script("arguments[0].scrollBy(0, 800);", viewport)
        time.sleep(random.uniform(0.5, 1.0))
    
    if not found_target_date:
        print("Fehler: Zieldatum nicht gefunden!")
        driver.quit()
        exit()

    time.sleep(3)

    arbeitsplatz_element = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Arbeitsplatz 09-3')]"))
    )
    print("Arbeitsplatz 09-3 gefunden!")
    
    time.sleep(2)

    # Scrolle das Element in den sichtbaren Bereich
    driver.execute_script("arguments[0].scrollIntoView(true);", arbeitsplatz_element)
    time.sleep(1)

    # Versuche, den "Schnelle Buchung" Link zu finden - mit mehreren Versuchen
    quick_book_link = None
    
    # Versuch 1: Im Card-Container suchen
    try:
        card_container = arbeitsplatz_element.find_element(By.XPATH, "ancestor::div[@data-testid='common--user-spaces-cards-card']")
        quick_book_link = card_container.find_element(By.XPATH, ".//a[@data-testid='common--user-spaces-cards-quick-book']")
        print("Schnelle Buchung Link gefunden (im Card-Container)!")
    except:
        print("Link nicht im Card-Container gefunden, versuche andere Methode...")
    
    # Versuch 2: Global mit WebDriverWait suchen
    if not quick_book_link:
        try:
            quick_book_link = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, ".//a[@data-testid='common--user-spaces-cards-quick-book']"))
            )
            print("Schnelle Buchung Link gefunden (global)!")
        except:
            print("Link konnte global nicht gefunden werden")
    
    # Versuch 3: Alle Links auflisten und nach Arbeitsplatz 09-3 suchen
    if not quick_book_link:
        try:
            all_cards = driver.find_elements(By.XPATH, "//div[@data-testid='common--user-spaces-cards-card']")
            print(f"Gefundene Cards: {len(all_cards)}")
            
            for card in all_cards:
                try:
                    workspace_name = card.find_element(By.XPATH, ".//*[contains(text(), 'Arbeitsplatz 09-3')]")
                    link = card.find_element(By.XPATH, ".//a[@data-testid='common--user-spaces-cards-quick-book']")
                    quick_book_link = link
                    print("Schnelle Buchung Link gefunden (in Card-Schleife)!")
                    break
                except:
                    pass
        except Exception as e:
            print(f"Fehler bei Card-Schleife: {e}")
    
    if quick_book_link:
        time.sleep(1)
        human_click(driver, quick_book_link)
        print("Schnelle Buchung erfolgreich geklickt!")

        time.sleep(2)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Gebucht')]"))
        )
        print("Buchung erfolgreich abgeschlossen!")

        time.sleep(2)

        print("Schliesse Browser...")
        driver.quit()
        print("Programm erfolgreich beendet!")
    else:
        print("FEHLER: Schnelle Buchung Link konnte nicht gefunden werden!")
        driver.quit()
        exit()

except TimeoutException as e:
    print(f"Timeout Fehler: {e}")
    driver.quit()
except Exception as e:
    print(f"Fehler: {e}")
    import traceback
    traceback.print_exc()
    driver.quit()

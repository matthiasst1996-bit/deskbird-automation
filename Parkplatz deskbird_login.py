import time
import random
import sys
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


# ========== KONFIGURATION ==========
PREFERRED_LOCATION = "Stellplatz 68"  # ← LIEBLINGS-STELLPLATZ
# ====================================

try:
    driver.get("https://app.deskbird.com/login/check-in")

    email_input = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.NAME, "email"))
    )
    human_typing(email_input, "Strotmann.M@proservicekoeln.de")
    time.sleep(random.uniform(1.5, 3.0))

    def wait_for_enabled_signin(driver):
        try:
            btn = driver.find_element(By.CSS_SELECTOR, "button.p-element.p-ripple.font-ProximaNovaBold.w-full.p-button.p-component")
            return btn if btn.is_enabled() else False
        except:
            return False
    
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

    print("✓ Login erfolgreich abgeschlossen!")
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
            print(f"✓ Zieldatum gefunden: {target_date_text}")
            found_target_date = True
            time.sleep(1)
            break
        except:
            pass
        
        driver.execute_script("arguments[0].scrollBy(0, 800);", viewport)
        time.sleep(random.uniform(0.5, 1.5))
    
    if not found_target_date:
        print("✗ Fehler: Zieldatum nicht gefunden!")
        driver.quit()
        sys.exit(1)

    time.sleep(3)

    # ===== FUNKTION ZUM BUCHEN =====
    def try_book_location(location_name):
        """Versucht einen Stellplatz zu buchen. Gibt True zurück wenn erfolgreich."""
        print(f"\n--- Versuche {location_name} zu buchen ---")
        
        try:
            # Suche das Element mit dem Location-Namen
            location_element = driver.find_element(By.XPATH, f"//*[contains(text(), '{location_name}')]")
            print(f"✓ Text '{location_name}' gefunden!")
        except:
            print(f"✗ Text '{location_name}' nicht gefunden!")
            return False

        time.sleep(1)
        driver.execute_script("arguments[0].scrollIntoView(true);", location_element)
        time.sleep(1.5)

        # Finde den Card-Container
        try:
            card_container = location_element.find_element(By.XPATH, "ancestor::div[@data-testid='common--user-spaces-cards-card']")
            print(f"✓ Card-Container gefunden!")
        except:
            print(f"✗ Card-Container nicht gefunden!")
            return False

        # Überprüfe ob Stellplatz BESETZT ist
        try:
            besetzt_element = card_container.find_element(By.XPATH, ".//*[contains(text(), 'Besetzt')]")
            print(f"✗ {location_name} ist BESETZT!")
            return False
        except:
            print(f"✓ {location_name} ist VERFÜGBAR!")

        time.sleep(1)

        # Suche "Schnelle Buchung" Button
        try:
            quick_book_link = card_container.find_element(By.XPATH, ".//a[@data-testid='common--user-spaces-cards-quick-book']")
            
            # Überprüfe ob Button clickbar ist
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable(quick_book_link))
            print(f"✓ 'Schnelle Buchung' Button gefunden und clickbar!")
        except:
            print(f"✗ 'Schnelle Buchung' Button nicht gefunden oder nicht clickbar!")
            return False

        # Klick auf den Button
        print(f"Klicke auf 'Schnelle Buchung' für {location_name}...")
        time.sleep(1)
        human_click(driver, quick_book_link)
        print(f"✓ Button geklickt!")

        time.sleep(3)

        # Warte auf Bestätigung
        try:
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Gebucht')]"))
            )
            print(f"✓✓✓ {location_name} erfolgreich gebucht!")
            return True
        except:
            print(f"✗ Keine Buchungsbestätigung!")
            return False

    # ===== HAUPTLOGIK =====
    print(f"\n=== Starte Buchungsprozess ===")
    booked = False

    # VERSUCH 1: Buche Lieblings-Stellplatz 68
    if try_book_location(PREFERRED_LOCATION):
        booked = True
    else:
        # VERSUCH 2: Wenn Stellplatz 68 nicht verfügbar, buche irgendeinen anderen Stellplatz
        print(f"\n{PREFERRED_LOCATION} nicht verfügbar. Suche anderen Stellplatz...")
        
        try:
            # Finde ALLE Stellplätze (nicht Arbeitsplätze!)
            all_cards = driver.find_elements(By.XPATH, "//div[@data-testid='common--user-spaces-cards-card']")
            print(f"Gefundene Cards: {len(all_cards)}")
            
            for idx, card in enumerate(all_cards):
                try:
                    # Suche Stellplätze (aber nicht Arbeitsplätze!)
                    # Suche nach "Stellplatz" im Card-Text
                    stellplatz_text = card.find_element(By.XPATH, ".//*[contains(text(), 'Stellplatz')]")
                    
                    # Überprüfe ob nicht "Besetzt"
                    try:
                        besetzt = card.find_element(By.XPATH, ".//*[contains(text(), 'Besetzt')]")
                        continue  # Überspinge diesen - er ist besetzt
                    except:
                        pass  # Gut, nicht besetzt
                    
                    # Versuche "Schnelle Buchung" zu finden
                    try:
                        quick_book = card.find_element(By.XPATH, ".//a[@data-testid='common--user-spaces-cards-quick-book']")
                        
                        # Scrolle zum Card
                        driver.execute_script("arguments[0].scrollIntoView(true);", card)
                        time.sleep(1)
                        
                        # Klick
                        print(f"\nBuche Stellplatz #{idx+1}...")
                        human_click(driver, quick_book)
                        print(f"✓ Button geklickt!")
                        
                        time.sleep(3)
                        
                        # Überprüfe Bestätigung
                        try:
                            WebDriverWait(driver, 15).until(
                                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Gebucht')]"))
                            )
                            print(f"✓✓✓ Stellplatz #{idx+1} erfolgreich gebucht!")
                            booked = True
                            break
                        except:
                            print(f"✗ Buchung fehlgeschlagen, versuche nächsten...")
                            continue
                    except:
                        continue
                except:
                    continue
        except Exception as e:
            print(f"Fehler beim Durchsuchen der Stellplätze: {e}")

    # ===== ERGEBNIS =====
    if booked:
        time.sleep(2)
        print("\n✓✓✓ ERFOLG: Stellplatz gebucht!")
        print("Schliesse Browser...")
        driver.quit()
        print("✓✓✓ Programm erfolgreich beendet!")
    else:
        print("\n✗✗✗ FEHLER: Keine Stellplätze verfügbar!")
        driver.quit()
        sys.exit(1)

except TimeoutException as e:
    print(f"✗ Timeout Fehler: {e}")
    driver.quit()
    sys.exit(1)
except Exception as e:
    print(f"✗ Fehler: {e}")
    import traceback
    traceback.print_exc()
    driver.quit()
    sys.exit(1)

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime

# Identifiants intranet :
USERNAME = "amoudrul" 
PASSWORD = "1#NLvaqmdoau3d!rou+0112"

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options)
driver.implicitly_wait(5)
driver.get("https://ade-usmb-ro.grenet.fr/direct/index.jsp")

time.sleep(1)

# Login
username_input = driver.find_element(By.CSS_SELECTOR, "input[name='username']")
password_input = driver.find_element(By.CSS_SELECTOR, "input[name='password']")
username_input.send_keys(USERNAME)
password_input.send_keys(PASSWORD)
time.sleep(0.5)
driver.find_element(By.CSS_SELECTOR, "button[name='submitBtn']").click()

time.sleep(1)

driver.find_element(By.XPATH, "//span[text()='Savoie2024-2025']").click()
driver.find_element(By.XPATH, "//button[text()='Ouvrir']").click()

time.sleep(1)

# Barre de recherche
search_input = None
inputs = driver.find_elements(By.TAG_NAME, "input")
for input in inputs:
    id = input.get_attribute("id")
    if id and id.startswith("x-auto-") and id.endswith("-input"):
        # Vérifie si un ancêtre possède un descendant <span> avec le texte 'RECHERCHE'
        ancestor = input
        for _ in range(4):
            ancestor = ancestor.find_element(By.XPATH, "..")
        spans = ancestor.find_elements(By.XPATH, ".//span[text()='RECHERCHE']")
        if spans:
            search_input = input
            break
if search_input is None:
    raise Exception("Barre de recherche introuvable")
else:
    print('Barre de recherche trouvée', search_input.get_attribute("id"))

search_input.send_keys("IDU-3-G1")
search_input.send_keys("\n")

print("Recherche")
time.sleep(2)

driver.find_elements(By.XPATH, "//span[contains(text(), 'IDU-3-G1')]")[0].click()

time.sleep(0.5)

# Transforme en tableau
# x_btn_images = driver.find_elements(By.CSS_SELECTOR, "img.x-btn-image")
# x_btn_images[-1].find_element(By.XPATH, "..").click()

# driver.find_element(By.XPATH, "//div[text()='Tableau_LLSH']").click()

# time.sleep(0.1)

# driver.find_element(By.XPATH, "//div[@title='Close']").click()

# Bouton exporter
x_btn_images = driver.find_elements(By.CSS_SELECTOR, "img.x-btn-image")
x_btn_images[-3].find_element(By.XPATH, "..").click()

# Sélectionne la date 
debut = driver.find_element(By.XPATH, "//label[text()='Date de début']")
debut_date = debut.find_element(By.XPATH, "..").find_element(By.TAG_NAME, "input")
debut_date.send_keys(f"01/01/{datetime.now().year}")

fin = driver.find_element(By.XPATH, "//label[text()='Date de fin']")
fin_date = fin.find_element(By.XPATH, "..").find_element(By.TAG_NAME, "input")
fin_date.send_keys(datetime.now().strftime("%d/%m/%Y"))

generer = driver.find_element(By.XPATH, "//button[text()='Générer URL']")
generer.click()

time.sleep(0.5)

# Récupère le premier lien a href commençant par
url = None
liens = driver.find_elements(By.TAG_NAME, "a")
for lien in liens:
    href = lien.get_attribute("href")
    if href and href.startswith("https://ade-usmb-ro.grenet.fr/jsp/custom/modules/plannings/direct_cal.jsp?data="):
        url = href
        break
    
print(url + "&nocache")

time.sleep(30)
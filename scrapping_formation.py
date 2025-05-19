import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Masquage
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

def get_formation_titles(url):

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)

    time.sleep(2)

    titles = []

    while True:
        # Balises a dont le le parent est h4 et qui contiennent le mot "catalogue"
        elements = driver.find_elements(By.CSS_SELECTOR, "h4>a[href*='/fr/catalogue']")
        
        # Liens des formations
        for element in elements:
            title = element.get_attribute('href')
            if title not in titles:  
                titles.append(title)

        try:
            time.sleep(2)  
            #Bouton "Suivant" 
            next_button = driver.find_element(By.CLASS_NAME, 'ametys-pagination__arrow_next')
            print("next_button", next_button)
            next_button.click() 
            
        except Exception as e:
            print(f"Plus de pages suivantes disponibles.\nErreur : {e}")
            break  

    driver.quit()
    return titles

def save_to_json(data, filename="output.json"):
    with open(filename, mode='w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


if __name__ == "__main__":

    url = "https://formations.univ-smb.fr/fr/rechercher.html"  # URL de la page
    titles = get_formation_titles(url)
    data = []

    print("Total des formations :", len(titles), "\n")
    for title in titles:
        data.append(title)
        print("-", title, "\n")

    # Enregistrer dans un JSON
    save_to_json(data)

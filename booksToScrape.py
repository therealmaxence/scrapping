from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import csv

# URL of the website
url = "https://books.toscrape.com/"

# Set up Chrome options for headless browsing and suppress unnecessary logs
options = Options()
options.add_argument("--disable-logging")
options.add_argument("--headless")  # Run in headless mode (no GUI)
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
options.add_argument(f"user-agent={headers['User-Agent']}")

def get_books_genre(url):
    """Scrape genres and their corresponding links from the website."""
    driver = webdriver.Chrome()
    
    driver.get(url)
    time.sleep(2)  

    # Genres
    genre_elements = driver.find_elements(By.CSS_SELECTOR, "ul.nav-list li ul li a")

    # Genre links
    genres = [genre.text.strip() for genre in genre_elements]
    genre_links = [genre.get_attribute('href') for genre in genre_elements]

    driver.quit()
    return genres, genre_links



def save_to_csv(file, genres, genre_links):
    """Save genres and links to a CSV file using write()."""
    with open(file, mode='w', encoding='utf-8', newline='') as f:
        f.write("Genre;Link\n")  
        for genre, link in zip(genres, genre_links):
            f.write(f"{genre};{link}\n")  



if __name__ == "__main__":
    genres, genre_links = get_books_genre(url)
    
    print("\nTotal genres:", len(genres), "\n")
    for genre, link in zip(genres, genre_links):
        print(f"{genre}: {link}\n")

    save_to_csv("books_genres.csv", genres, genre_links)
    print("✅ Genre links saved to books_genres.csv")

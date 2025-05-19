from bs4 import BeautifulSoup
import requests
from unidecode import unidecode
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import Keys
from selenium.webdriver.support import expected_conditions as EC

class MCC_Spyder:
    def __init__(self, timeout=10):
        self.default_url = "https://formations.univ-smb.fr/fr/rechercher.html#nav"
        self.driver = webdriver.Edge()
        self.timeout = timeout

    def getall_degree(self):
        self.driver.get(self.default_url)
        degrees = []
        next_page_available = True
        while next_page_available:
            degree_links = WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "h4>a[href*='/fr/catalogue']"))
            )

            for a in degree_links:
                try:
                    degrees.append({'formation': a.text, 'link': a.get_attribute('href'), 'mcc': None })
                except Exception as e:
                    print(e)
                
            next_page_available = self.__pagination_next__()
        return degrees

    def __pagination_next__(self):
        try:
            next_page = WebDriverWait(self.driver, self.timeout).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".ametys-pagination>li>a[value='Suivant']"))
            )
            ActionChains(self.driver)\
                .move_to_element(next_page)\
                .click()\
                .perform()
            time.sleep(1) # wait for the page to load
            return True
        except Exception as e:
            return False
        
    # BeautifulSoup
    def get_mcc_degree(self, url):
        mcc = []
        self.driver.get(url)
        years = WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#programmeBadges>div"))
        )
        for y, year in enumerate(years):
            try:
                ActionChains(self.driver)\
                .move_to_element(year)\
                .click()\
                .perform()
                time.sleep(1) # wait for the page to load
                mcc.append({
                    'year': year.find_element(By.CSS_SELECTOR, "label>span").text,
                    'program' : []
                })

                semesters = WebDriverWait(self.driver, self.timeout).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[id*='tab-content'].active>div>nav>ul>li>a[href*='#semester']:not(.disable)"))
                )
                for s, semester in enumerate(semesters):
                    try:
                        ActionChains(self.driver)\
                            .move_to_element(semester)\
                            .click()\
                            .perform()
                        time.sleep(1) # wait for the page to load
                        mcc[y]['program'].append({'semestre': semester.text, 'modules' : []})
                        modules = WebDriverWait(self.driver, self.timeout).until(
                            EC.presence_of_all_elements_located((By.CSS_SELECTOR, f"#{semester.get_attribute('href').split("#")[-1]}>ul>li"))
                        )
                        for module in modules:
                            module_name = module.find_element(By.CSS_SELECTOR, "header>h2>a").text
                            credit = module.find_element(By.CSS_SELECTOR, "header>span").text
                            mcc[y]['program'][s]['modules'].append({
                                'module': module_name,
                                'credit': credit
                            })
                    except Exception as e:
                        print(e)
                        mcc[y]['program'][s]['modules'].append({
                            'module': None,
                            'credit': None
                        })
            except Exception as e:
                print(e)
                mcc.append({
                    'year': None,
                    'program' : []
                })
        return mcc


    # def get_catalogue(self, pathway, url=None):
    #     if url is None:
    #         url = self.default_url
    #     response = requests.get(url)
    #     pathway = unidecode(pathway.lower().replace(" ", "-").replace(",", ""))
    #     soup = BeautifulSoup(response.text, 'html.parser')
    #     print(soup)
    #     hyperlinks = [
    #         a for a in soup.find_all("a", href=True)
    #         if not a.has_attr("class")
    #     ]
    #     # for a in hyperlinks:
    #     #     print(a["href"])
    #     return soup
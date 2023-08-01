from selenium import webdriver

from selenium.webdriver.common.by import By

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Scraper():
    def __init__(self):
        self._scraper = webdriver.Chrome()
    
    def navigate_to_form(self):
        self._scraper.get('https://www.pandaguestexperience.com/')
        button = self._scraper.find_element(By.ID, "NextButton")

        while button and ("100" not in self._scraper.title):
            button.click()
            try:
                button = WebDriverWait(self._scraper, 10).until(
                    EC.presence_of_element_located((By.ID, "NextButton"))
                )
            except:
                self._scraper.quit()

    def fill_form(self, email_addr):
        self._scraper.find_element(By.XPATH, "//input[@id='S000057']").send_keys(email_addr)
        self._scraper.find_element(By.XPATH, "//input[@id='S000064']").send_keys(email_addr)
        self._scraper.find_element(By.ID, "NextButton").click()
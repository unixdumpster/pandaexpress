from selenium import webdriver

from selenium.webdriver.common.by import By

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from email_utils import generate_email

class Scraper():
    def __init__(self, addr):
        self._scraper = webdriver.Chrome()
        self._addr = addr
    
    def autofill_form(self, max_iter):
        iter = 0
        while iter < max_iter:
            self._scraper.get('https://www.pandaguestexperience.com/')
            button = self._scraper.find_element(By.ID, "NextButton")

            # navigation
            while button and ("100" not in self._scraper.title):
                button.click()
                try:
                    button = WebDriverWait(self._scraper, 10).until(
                        EC.presence_of_element_located((By.ID, "NextButton"))
                    )
                except:
                    self._scraper.quit()
            
            # fill in form
            self._scraper.find_element(By.XPATH, "//input[@id='S000057']").send_keys(self._addr)
            self._scraper.find_element(By.XPATH, "//input[@id='S000064']").send_keys(self._addr)
            self._scraper.find_element(By.ID, "NextButton").click()

            iter = iter + 1
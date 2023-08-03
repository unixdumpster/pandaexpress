import re
import requests

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

def main():

    scraper = webdriver.Chrome()
    scraper.get('https://www.pandaguestexperience.com/')
    button = scraper.find_element(By.ID, "NextButton")

    # navigation
    while button and ("100" not in scraper.title):
        button.click()
        try:
            button = WebDriverWait(scraper, 10).until(
                EC.presence_of_element_located((By.ID, "NextButton"))
            )
        except:
           scraper.quit()
    
    # fill in form using generated email
    addr = generate_email()
    scraper.find_element(By.XPATH, "//input[@id='S000057']").send_keys(self._addr)
    scraper.find_element(By.XPATH, "//input[@id='S000064']").send_keys(self._addr)
    scraper.find_element(By.ID, "NextButton").click()

    # retrive discount code from inbox
    login, domain = addr.split("@")[0], addr.split("@")[1]

    code_html = get_code(login, domain)
    parse_code(code_html)

def generate_email():
    URL = 'https://www.1secmail.com/api/v1/'
    payload = {'action': 'genRandomMailbox', 'count': 1}
    r = requests.get(URL, payload)
    email = r.json()
    return email[0]

def get_code(login, domain):
    URL = 'https://www.1secmail.com/api/v1/'
    payload = {'action': 'getMessages', 'login': login, 'domain': domain}

    while True:
        message = requests.get(URL, payload).json()[0]
        if message:
            break
    
    # scan individual messages for codes (in HTML format)
    payload['action'] = 'readMessage'
    id = message['id']
    payload['id'] = id
    html_body = requests.get(URL, payload).json()['body']
    
    return html_body

def parse_code(code_html):
    pattern = r'<span class="coupon-code" style="font-family:\'Montserrat\', Arial, sans-serif !important;">(.*?)</span>'

    match = re.findall(pattern, code_html)
    if match:
        print("Code:", match)


if __name__ == '__main__':
    main()
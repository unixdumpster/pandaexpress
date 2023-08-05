import re
import requests
from tempfile import mkdtemp
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

def handler(event=None, context=None):
    options = webdriver.ChromeOptions()
    options.binary_location = '/opt/chrome/chrome'
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1280x1696")
    options.add_argument("--single-process")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-dev-tools")
    options.add_argument("--no-zygote")
    options.add_argument(f"--user-data-dir={mkdtemp()}")
    options.add_argument(f"--data-path={mkdtemp()}")
    options.add_argument(f"--disk-cache-dir={mkdtemp()}")
    options.add_argument("--remote-debugging-port=9222")
    scraper = webdriver.Chrome("/opt/chromedriver",
                              options=options)

    # navigation
    scraper.get('https://www.pandaguestexperience.com/')
    button = scraper.find_element(By.ID, "NextButton")
    while button and ("100" not in scraper.title):
        button.click()
        try:
            button = WebDriverWait(scraper, 3).until(
                EC.presence_of_element_located((By.ID, "NextButton"))
            )
        except:
           scraper.close()
           scraper.quit()
           return {"statusCode": 100, "body": "FAIL"}
    
    # # # fill in form using generated email
    addr = generate_email()
    scraper.find_element(By.XPATH, "//input[@id='S000057']").send_keys(addr)
    scraper.find_element(By.XPATH, "//input[@id='S000064']").send_keys(addr)
    scraper.find_element(By.ID, "NextButton").click()

    # retrive discount code from inbox
    login, domain = addr.split("@")[0], addr.split("@")[1]

    code_html = get_code(login, domain)
    code = parse_code(code_html)

    scraper.close()
    scraper.quit()
    response = {
        "statusCode": 200,
        "body": code
    }

    return response

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
        message = requests.get(URL, payload).json()
        if message:
            break
    
    message = message[0]
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
        return match
    
    return None

if __name__ == '__main__':
    main()
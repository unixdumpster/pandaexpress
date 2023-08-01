import requests

def parse_codes(addr, domain):
    url = 'https://www.1secmail.com/api/v1/'
    payload = {'action': 'getMessages', 'login': addr, 'domain': domain}

    r = requests.get(url, payload)
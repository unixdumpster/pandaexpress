import requests

def generate_email():
    url = 'https://www.1secmail.com/api/v1/'
    payload = {'action': 'genRandomMailbox', 'count': 1}

    r = requests.get(url, payload)
    email = r.json()
    return email
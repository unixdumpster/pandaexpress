import requests

URL = 'https://www.1secmail.com/api/v1/'

def generate_email():
    payload = {'action': 'genRandomMailbox', 'count': 1}
    r = requests.get(URL, payload)
    email = r.json()
    return email[0]

def get_codes(login, domain):
    payload = {'action': 'getMessages', 'login': login, 'domain': domain}

    while True:
        messages = requests.get(URL, payload).json()
        if messages:
            break
    
    # scan individual messages for codes (in HTML format)
    codes_html = []
    payload['action'] = 'readMessage'
    print(len(messages))
    for message in messages:
        id = message['id']
        payload['id'] = id
        html_body = requests.get(URL, payload).json()['body']
        codes_html.append(html_body)

    return codes_html


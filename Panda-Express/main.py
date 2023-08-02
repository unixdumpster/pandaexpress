import sys
import re
from api.classes import Scraper
from email_utils import generate_email, get_codes

def main():
    
    if len(sys.argv) != 2:
        usage()

    max_iter = int(sys.argv[1])

    addr = generate_email()
    login, domain = addr.split("@")[0], addr.split("@")[1]

    scraper = Scraper(addr)
    scraper.autofill_form(max_iter)

    codes_html = get_codes(login, domain)
    parse_codes(codes_html)

def parse_codes(codes_html):
    pattern = r'<span class="coupon-code" style="font-family:\'Montserrat\', Arial, sans-serif !important;">(.*?)</span>'

    for idx, code in enumerate(codes_html):
        match = re.findall(pattern, code)
        if match:
            print("Code #", idx + 1, ":", match)

def usage():
    pass

if __name__ == '__main__':
    main()
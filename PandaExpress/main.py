from scraper_utils import Scraper
import email_utils
import os
import sys

def main():
    
    if len(sys.argv) != 2:
        usage()

    max_iter = int(sys.argv[1])
    email_addr = email_utils.generate_email()
    scraper = Scraper()

    iter = 0
    while iter < max_iter:
        scraper.navigate_to_form()
        scraper.fill_form(email_addr)
        iter = iter + 1
    
    email_addr = str(email_addr)
    print(email_addr)
    email_utils.parse_codes(email_addr.split("@")[0], email_addr.split("@")[1])


def usage():
    pass

if __name__ == '__main__':
    main()
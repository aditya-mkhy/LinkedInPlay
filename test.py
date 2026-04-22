import requests
import re
from bs4 import BeautifulSoup

def parse_login_response(html):
    html = html.lower()

    if "bad password" in html:
        return "BAD_PASSWORD"

    elif "wait for 1 min" in html:
        return "LOCKED_1_MIN"

    elif "logout" in html:
        return "SUCCESS"

    return "UNKNOWN"

ROUTER = "http://192.168.1.1"
USERNAME = "admin"
PASSWORD = "12345678"

s = requests.Session()

headers = {
    "User-Agent": "Mozilla/5.0",
    "Referer": ROUTER + "/admin/login.asp"
}

# Step 1: Load login page
r = s.get(ROUTER + "/admin/login.asp", headers=headers)
html = r.text

# Step 2: Extract csrf token
soup = BeautifulSoup(html, "html.parser")
csrf = soup.find("input", {"name": "csrftoken"})["value"]

# Step 3: Extract verification code from JS
match = re.search(r"check_code'\)\.value='(.*?)'", html)

if match:
    verification_code = match.group(1)
else:
    raise Exception("Verification code not found")

print("CSRF:", csrf)
print("Verification:", verification_code)

# Step 4: Login
payload = {
    "username": USERNAME,
    "psd": PASSWORD,
    "sec_lang": "0",
    "loginSelinit": "0",
    "ismobile": "0",
    "verification_code": verification_code,
    "csrftoken": csrf
}

r = s.post(
    ROUTER + "/boaform/admin/formLogin",
    data=payload,
    headers=headers
)

print("Status:", r.status_code)
print(r.text)

status = parse_login_response(r.text)
print(status)

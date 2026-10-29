# Shared constants and helpers 

BASE_URL = "http://zero.webappsecurity.com"
VALID_USER = "username"
VALID_PASS = "password"


#Navigate to a page with retries if navigation fails.
def safe_goto(page, path: str, tries: int = 4):
    last = None
    for _ in range(tries):
        try:
            return page.goto(path, wait_until="load", timeout=45000)          # 45 secs
        except Exception as e: 
            last = e
            page.wait_for_timeout(1500)                                       # 1.5 sec wait before retrying
    raise last                                                     # Raise the last error if all attempts fail



#Log in and navigate to the account summary page.
def login(page, user: str = VALID_USER, pw: str = VALID_PASS):
    safe_goto(page, "/login.html")
    page.fill("#user_login", user)                                    # Enter login credentials
    page.fill("#user_password", pw)
    page.click('input[type="submit"][value="Sign in"]')
    page.wait_for_load_state("load")

    if "accept-certs" in page.url:                                 # Handle certificate page if it appears
        cont = page.locator(
            'input[type="submit"], button[type="submit"], a.btn'
        ).first
        if cont.count():
            cont.click()
            page.wait_for_load_state("load")
    safe_goto(page, "/bank/account-summary.html")


def is_authenticated(page) -> bool:
    return "login.html" not in page.url
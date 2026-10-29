from helpers import login, is_authenticated, safe_goto

# assert login endpoint in url and account summary page is visible after login
def test_login_valid_credentials(page):
    login(page)
    assert is_authenticated(page), "valid credentials should authenticate"
    assert "account" in page.locator("body").inner_text().lower()


#  incorrect password 
def test_login_invalid_credentials(page):
    safe_goto(page, "/login.html")
    page.fill("#user_login", "username")
    page.fill("#user_password", "wrong-password")
    page.click('input[type="submit"][value="Sign in"]')
    page.wait_for_load_state("load")
    safe_goto(page, "/bank/account-summary.html")
    assert "login.html" in page.url, "bad credentials must not authenticate"


# empty login fields
def test_login_empty_submission(page):
    safe_goto(page, "/login.html")
    page.click('input[type="submit"][value="Sign in"]')
    page.wait_for_load_state("load")
    safe_goto(page, "/bank/account-summary.html")
    assert "login.html" in page.url, "empty login must not authenticate"
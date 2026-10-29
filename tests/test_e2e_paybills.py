import pytest
from helpers import login, safe_goto

SUCCESS = "successfully"  # Text used to identify a successful payment message


@pytest.fixture
def paybills_page(page):
    login(page)
    safe_goto(page, "/bank/pay-bills.html")
    page.select_option("#sp_payee", index=1)                # select second option in dropdown
    page.select_option("#sp_account", index=1)
    page.fill("#sp_date", "2026-12-01")
    return page

#valid payment
def test_paybills_valid_payment_succeeds(paybills_page):
    page = paybills_page
    page.fill("#sp_amount", "50")
    page.click("#pay_saved_payees")
    page.wait_for_load_state("load")
    assert SUCCESS in page.locator("body").inner_text().lower()


# empty amount
def test_paybills_empty_amount_rejected(paybills_page):
    page = paybills_page
    page.fill("#sp_amount", "")
    page.click("#pay_saved_payees")
    page.wait_for_load_state("load")
    assert SUCCESS not in page.locator("body").inner_text().lower()


# non-numeric amount, expected marker fail
@pytest.mark.xfail(reason="Zero Bank BUG: non-numeric bill amount is accepted", strict=False)
def test_paybills_invalid_amount_rejected(paybills_page):
    page = paybills_page
    page.fill("#sp_amount", "xyz")
    page.click("#pay_saved_payees")
    page.wait_for_load_state("load")
    assert SUCCESS not in page.locator("body").inner_text().lower()
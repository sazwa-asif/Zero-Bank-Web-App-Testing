import pytest
from helpers import login, safe_goto


@pytest.fixture
def transfer_page(page):
    login(page)
    safe_goto(page, "/bank/transfer-funds.html")
    page.select_option("#tf_fromAccountId", index=0)
    page.select_option("#tf_toAccountId", index=1)
    return page


# valid amount, takes to verify page
def test_transfer_valid_amount_reaches_review(transfer_page):
    page = transfer_page
    page.fill("#tf_amount", "25")
    page.fill("#tf_description", "e2e-positive")
    page.click("#btn_submit")
    page.wait_for_load_state("load")
    assert "verify" in page.url.lower(), "valid transfer should reach the verify step"

#empty amount
def test_transfer_empty_amount_rejected(transfer_page):
    page = transfer_page
    page.fill("#tf_amount", "")
    page.click("#btn_submit")
    page.wait_for_load_state("load")
    assert "verify" not in page.url.lower(), "empty amount must not advance"


# non-numeric amount, expected marker fail
@pytest.mark.xfail(reason="Zero Bank BUG: non-numeric transfer amount is accepted", strict=False)
def test_transfer_invalid_amount_rejected(transfer_page):
    page = transfer_page
    page.fill("#tf_amount", "abc")
    page.click("#btn_submit")
    page.wait_for_load_state("load")
    assert "verify" not in page.url.lower(), "non-numeric amount should be rejected"


import pytest
from test_e2e_paybills import paybills_page

SUCCESS = "successfully"


@pytest.mark.planted_bug
def test_paybills_invalid_amount_rejected(paybills_page):
    page = paybills_page

    # Enter a non-numeric payment amount
    page.fill("#sp_amount", "xyz")
    page.click("#pay_saved_payees")
    page.wait_for_load_state("load")

    # The website should reject the invalid amount
    assert SUCCESS not in page.locator("body").inner_text().lower(), (
        "Planted bug detected: the website accepted a non-numeric payment amount."
    )

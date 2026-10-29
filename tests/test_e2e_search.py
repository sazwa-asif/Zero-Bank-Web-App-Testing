from helpers import safe_goto

# page contains either online or results
def test_search_returns_results_page(page):
    safe_goto(page, "/search.html?searchTerm=online")
    body = page.locator("body").inner_text().lower()             #text on page is stored in body
    assert "online" in body or "results" in body


#empty search term 
def test_search_empty_term_is_handled(page):
    safe_goto(page, "/search.html?searchTerm=")                  # inspect search bar id
    assert page.locator("#searchTerm").is_visible()

#no results 
def test_search_no_results_message(page):
    safe_goto(page, "/search.html?searchTerm=zzzznomatch12345")
    assert "no results were found" in page.locator("body").inner_text().lower()


# empty search results show status 200
def test_mock_empty_search_results(page):
    def handle(route):
        route.fulfill(
            status=200,
            content_type="text/html",
            body="<html><body><h3>No results were found.</h3></body></html>",
        )
    page.route("**/search.html*", handle)
    page.goto("/search.html?searchTerm=anything")
    assert "no results were found" in page.locator("body").inner_text().lower()


# login page shows a 500 server error
def test_mock_server_error_on_login(page):
    def handle(route):
        route.fulfill(
            status=500,
            content_type="text/html",
            body="<html><body><h1>500 - Server Error</h1></body></html>",
        )
    page.route("**/login.html", handle)
    response = page.goto("/login.html")
    assert response is not None and response.status == 500
    assert "server error" in page.locator("body").inner_text().lower()

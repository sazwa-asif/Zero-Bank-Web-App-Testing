# API tests CRUD operations on login

def test_read_get(api_context):
    assert api_context.get("/login.html").status == 200
    assert api_context.get("/no-such-page-404-check.html").status == 404


def test_create_post_signin(api_context):
    resp = api_context.post("/signin.html",form={"user_login": "username", "user_password": "password", "submit": "Sign in"},max_redirects=0,)
    assert resp.status in (200, 302), f"expected 200/302 from POST, got {resp.status}"


def test_update_put(api_context):
    assert api_context.put("/login.html").status == 200
    assert api_context.put("/no-such-page-404-check.html").status == 404


def test_delete(api_context):
    assert api_context.delete("/login.html").status == 200
    assert api_context.delete("/no-such-page-404-check.html").status == 404
# fixtures and hooks

import pathlib
import pytest
from helpers import BASE_URL


#hook
def pytest_runtest_makereport(item, call):
    if call.when != "call":          # take ss only when executing not setup/teardown
        return

    page = item.funcargs.get("page")
    if page is None:
        return  # Skip API tests without a browser page

    try:
        shots = pathlib.Path(item.config.rootdir) / "screenshots"
        shots.mkdir(exist_ok=True)
        page.screenshot(path=str(shots / f"{item.name}.png"), full_page=True)
    except Exception:
        pass  # Ignore screenshot errors so tests can finish


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    # Set browser size and ignore HTTPS certificate errors
    return {
        **browser_context_args,
        "viewport": {"width": 1280, "height": 720},
        "ignore_https_errors": True,
    }


@pytest.fixture
def api_context(playwright):
    # Create an API request context and clean it up after the test
    ctx = playwright.request.new_context(
        base_url=BASE_URL,
        ignore_https_errors=True
    )
    yield ctx
    ctx.dispose()
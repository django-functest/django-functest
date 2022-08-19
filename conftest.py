SHOW_BROWSER = False
SIGNED_COOKIES = False


def pytest_addoption(parser):
    parser.addoption("--show-browser", action="store_true", default=False, help="Show web browser window")
    parser.addoption("--signed-cookies", action="store_true", default=False, help="Use signed cookies session backend")


def pytest_configure(config):
    global SHOW_BROWSER, SIGNED_COOKIES
    SHOW_BROWSER = config.option.show_browser
    SIGNED_COOKIES = config.option.signed_cookies

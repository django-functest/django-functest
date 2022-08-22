BROWSER = "Firefox"
SHOW_BROWSER = False


def pytest_addoption(parser):
    parser.addoption(
        "--browser", type=str, default="Firefox", help="Selenium driver_name to use", choices=["Firefox", "Chrome"]
    )
    parser.addoption("--show-browser", action="store_true", default=False, help="Show web browser window")


def pytest_configure(config):
    global SHOW_BROWSER, BROWSER
    BROWSER = config.option.browser
    SHOW_BROWSER = config.option.show_browser

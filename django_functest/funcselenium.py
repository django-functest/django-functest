from django.core.urlresolvers import reverse
from pyvirtualdisplay import Display
from selenium import webdriver


class FuncSeleniumMixin(object):

    @classmethod
    def setUpClass(cls):

        if not cls.show_browser():
            cls.__display = Display(visible=False)
            cls.__display.start()
        driver_name = cls.get_driver_name()
        kwargs = {}
        if driver_name == 'Firefox':
            from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
            profile = FirefoxProfile()
            # Firefox 29 does not support sending keystrokes to <input type=number> widgets
            # so we disable the special widgets.
            profile.set_preference('dom.forms.number', False)
            kwargs['firefox_profile'] = profile
        cls._driver = getattr(webdriver, driver_name)(**kwargs)
        if hasattr(cls._driver, 'profile'):
            # Firefix
            cls._driver.profile.set_preference('dom.forms.number', False)
        timeout = cls.get_default_timeout()
        cls._driver.implicitly_wait(timeout)
        cls._driver.set_page_load_timeout(timeout)

        super(FuncSeleniumMixin, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        if not cls.show_browser():
            cls._driver.quit()
            cls.__display.stop()
        super(FuncSeleniumMixin, cls).tearDownClass()


    # Common API:
    is_full_browser_test = True

    def get_url(self, name, *args, **kwargs):
        """
        Gets the named URL, passing *args and **kwargs to Django's URL 'reverse' function.
        """
        kwargs.pop('expect_errors', None)
        self.get_literal_url(reverse(name, args=args, kwargs=kwargs))
        # TODO - need tests
        #self.wait_until_loaded('body')
        #self.wait_for_ajax()

    def get_literal_url(self, url):
        """
        Gets the passed in URL, as a literal relative URL, without using reverse.
        """
        self._get_url_raw(self.live_server_url + url)

    @property
    def current_url(self):
        return self._driver.current_url

    # Full browser specific:


    # Configuration:
    display = False

    @classmethod
    def get_driver_name(cls):
        return "Firefox"  # Sensible default

    @classmethod
    def get_default_timeout(cls):
        return 10  # seconds

    @classmethod
    def show_browser(cls):
        return cls.display

    # Implementation methods - private
    def _get_url_raw(self, url):
        """
        'raw' method for getting URL - not compatible between FullBrowserTest and WebTestBase
        """
        self._have_visited_page = True
        self._driver.get(url)

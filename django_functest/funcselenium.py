from django.conf import settings
from django.core.urlresolvers import reverse
from pyvirtualdisplay import Display
from selenium import webdriver

from .utils import get_session_store


class FuncSeleniumMixin(object):

    @classmethod
    def setUpClass(cls):

        if not cls.display_browser_window():
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
        if not cls.display_browser_window():
            cls._driver.quit()
            cls.__display.stop()
        super(FuncSeleniumMixin, cls).tearDownClass()

    def setUp(self):
        self._have_visited_page = False
        super(FuncSeleniumMixin, self).setUp()
        self._driver.delete_all_cookies()

    # Common API:
    is_full_browser_test = True

    def get_url(self, name, *args, **kwargs):
        """
        Gets the named URL, passing *args and **kwargs to Django's URL 'reverse' function.
        """
        kwargs.pop('expect_errors', None)
        self.get_literal_url(reverse(name, args=args, kwargs=kwargs))
        # TODO - need tests
        # self.wait_until_loaded('body')
        # self.wait_for_ajax()

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
    display = False  # Display browser window or not?

    default_timeout = 10  # seconds

    driver_name = "Firefox"  # Sensible default, works most places

    @classmethod
    def display_browser_window(cls):
        return cls.display

    @classmethod
    def get_default_timeout(cls):
        return cls.default_timeout

    @classmethod
    def get_driver_name(cls):
        return cls.driver_name

    # Implementation methods - private
    def _get_url_raw(self, url):
        """
        'raw' method for getting URL - not compatible between FullBrowserTest and WebTestBase
        """
        self._have_visited_page = True
        self._driver.get(url)

    def add_cookie(self, cookie_dict):
        self._driver.add_cookie(cookie_dict)

    def set_session_vars(self, item_dict):
        # Cookies don't work unless we visit a page first
        if not self._have_visited_page:
            self.get_url('django_functest.emptypage')

        session = self.get_session()
        for name, value in item_dict.items():
            session[name] = unicode(value)
        session.save()

        s2 = self.get_session()
        if all(s2.get(name) == unicode(value) for name, value in item_dict.items()):
            return

        raise RuntimeError("Session not saved correctly")

    def get_session(self):
        session_cookie = self._driver.get_cookie(settings.SESSION_COOKIE_NAME)
        if session_cookie is None:
            # Create new
            session = get_session_store()
            self.add_cookie({'name': settings.SESSION_COOKIE_NAME,
                             'value': session.session_key,
                             'path': '/',
                             'secure': False,
                             })
        else:
            session = get_session_store(session_key=session_cookie['value'])
        return session

import logging
import time

from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.html import escape
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, NoSuchWindowException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select, WebDriverWait
from six import text_type

from .exceptions import SeleniumCantUseElement
from .utils import CommonMixin, get_session_store

logger = logging.getLogger(__name__)


class FuncSeleniumMixin(CommonMixin):

    @classmethod
    def setUpClass(cls):
        if not cls.display_browser_window():
            cls.__display = Display(visible=False)
            cls.__display.start()
        driver_name = cls.get_driver_name()
        kwargs = {}
        cls._driver = getattr(webdriver, driver_name)(**kwargs)
        timeout = cls.get_default_timeout()
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
        size = self.get_browser_window_size()
        if size is not None:
            self.set_window_size(*size)
        self._driver.delete_all_cookies()

    # Common API:
    is_full_browser_test = True

    def assertTextPresent(self, text):
        self.assertIn(escape(text), self._get_page_source())

    def assertTextAbsent(self, text):
        self.assertNotIn(escape(text), self._get_page_source())

    def back(self):
        self._driver.back()

    @property
    def current_url(self):
        return self._driver.current_url

    def follow_link(self, css_selector):
        return self.click(css_selector, wait_for_reload=True)

    def fill(self, fields):
        for k, v in fields.items():
            e = self._find_with_timeout(k)
            self._fill_input(e, v)

    def fill_by_text(self, fields):
        for selector, text in fields.items():
            elem = self._find_with_timeout(selector)
            self._fill_input_by_text(elem, text)

    def get_url(self, name, *args, **kwargs):
        """
        Gets the named URL, passing *args and **kwargs to Django's URL 'reverse' function.
        """
        kwargs.pop('expect_errors', None)
        self.get_literal_url(reverse(name, args=args, kwargs=kwargs))
        self.wait_until_loaded('body')
        # TODO - need tests
        # self.wait_for_ajax()

    def get_literal_url(self, url):
        """
        Gets the passed in URL, as a literal relative URL, without using reverse.
        """
        self._get_url_raw(self.live_server_url + url)

    def is_element_present(self, css_selector):
        try:
            self._driver.find_element_by_css_selector(css_selector)
        except NoSuchElementException:
            return False
        return True

    def submit(self, css_selector, wait_for_reload=True, auto_follow=None):
        self.click(css_selector, wait_for_reload=wait_for_reload)

    def value(self, css_selector):
        elem = self._find(css_selector)
        if elem.tag_name == 'input' and elem.get_attribute('type') == 'checkbox':
            return self._is_checked(elem)
        elif elem.tag_name == 'textarea':
            return elem.text
        else:
            return elem.get_attribute('value')

    # Full browser specific:

    # Configuration methods and attributes
    browser_window_size = None

    display = False  # Display browser window or not?

    default_timeout = 10  # seconds

    driver_name = "Firefox"  # Sensible default, works most places

    def get_browser_window_size(self):
        return self.browser_window_size

    @classmethod
    def display_browser_window(cls):
        return cls.display

    @classmethod
    def get_default_timeout(cls):
        return cls.default_timeout

    @classmethod
    def get_driver_name(cls):
        return cls.driver_name

    # Runtime methods:

    def click(self, css_selector=None, xpath=None, wait_for_reload=False, double=False, scroll=True):
        if wait_for_reload:
            self._driver.execute_script("document.pageReloadedYetFlag='notyet';")

        if xpath is not None:
            elem = self._driver.find_element_by_xpath(xpath)
        else:
            elem = self._find_with_timeout(css_selector)
        if scroll:
            self._scroll_into_view(elem)
        elem.click()
        if double:
            elem.click()

        if wait_for_reload:
            def f(driver):
                obj = driver.execute_script("return document.pageReloadedYetFlag;")

                if obj is None or obj != "notyet":
                    return True
                return False
            WebDriverWait(self._driver, self.get_default_timeout()).until(f)
        self._wait_until_finished()

    def execute_script(self, script, *args):
        return self._driver.execute_script(script, *args)

    def hover(self, css_selector):
        elem = self._find(css_selector)
        self._scroll_into_view(elem)
        ActionChains(self._driver).move_to_element(elem).perform()

    def is_element_displayed(self, css_selector):
        try:
            elem = self._driver.find_element_by_css_selector(css_selector)
        except NoSuchElementException:
            return False
        return elem.is_displayed()

    def set_window_size(self, width, height):
        self._driver.set_window_size(width, height)
        t = 0
        PAUSE = 0.1
        timeout = self.get_default_timeout()
        while t < timeout:
            win_width, win_height = self.execute_script("return [window.outerWidth, window.outerHeight]")
            if (win_width, win_height) == (width, height):
                return
            t += PAUSE
            time.sleep(PAUSE)
        logger.warning("Browser window was not resized to (%s, %s) after waiting %s seconds.", width, height, timeout)

    def wait_for_page_load(self):
        self.wait_until_loaded('body')
        self._wait_for_document_ready()

    def wait_until(self, callback, timeout=None):
        """
        Helper function that blocks the execution of the tests until the
        specified callback returns a value that is not falsy. This function can
        be called, for example, after clicking a link or submitting a form.
        See the other public methods that call this function for more details.
        """
        if timeout is None:
            timeout = self.get_default_timeout()
        WebDriverWait(self._driver, timeout).until(callback)

    def wait_until_loaded(self, selector, timeout=None):
        """
        Helper function that blocks until the element with the given tag name
        is found on the page.
        """
        self.wait_until(
            lambda driver: driver.find_element_by_css_selector(selector),
            timeout=timeout
        )

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
            session[name] = text_type(value)
        session.save()

        s2 = self.get_session()
        if all(s2.get(name) == text_type(value) for name, value in item_dict.items()):
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

    def _wait_for_document_ready(self):
        self.wait_until(lambda driver: driver.execute_script("return document.readyState") == "complete")

    def _wait_until_finished(self):
        try:
            self.wait_for_page_load()
        except NoSuchWindowException:
            pass  # window can legitimately close e.g. for popups

    def _get_page_source(self):
        return self._driver.page_source

    def _fill_input(self, elem, val):
        if elem.tag_name == 'select':
            self._set_select_elem(elem, val)
        elif elem.tag_name == 'input' and elem.get_attribute('type') == 'checkbox':
            self._set_check_box(elem, val)
        else:
            self._scroll_into_view(elem)
            elem.clear()
            elem.send_keys(val)

    def _fill_input_by_text(self, elem, val):
        if elem.tag_name == 'select':
            self._set_select_elem_by_text(elem, val)
        else:
            raise SeleniumCantUseElement("Can't do 'fill_by_text' on elements of type {0}".format(elem.tag_name))

    def _find(self, css_selector):
        return self._driver.find_element_by_css_selector(css_selector)

    def _find_with_timeout(self, css_selector, timeout=None):
        self.wait_until_loaded(css_selector, timeout=timeout)
        return self._find(css_selector)

    def _scroll_into_view(self, elem, attempts=0):
        if self._is_visible(elem):
            return

        # Attempt to scroll to the center of the screen. This is the best
        # location to avoid fixed navigation bars which tend to be at the
        # top and bottom.
        viewport_width, viewport_height, doc_width, doc_height = self._scroll_center_data()
        elem_x, elem_y = elem.location['x'], elem.location['y']
        elem_w, elem_h = elem.size['width'], elem.size['height']
        scroll_to_x = elem_x + elem_w / 2 - viewport_width / 2
        scroll_to_y = elem_y + elem_h / 2 - viewport_height / 2

        def clip(val, min_val, max_val):
            return max(min(val, max_val), min_val)

        scroll_to_x = clip(scroll_to_x, 0, doc_width)
        scroll_to_y = clip(scroll_to_y, 0, doc_height)

        self._driver.execute_script("window.scrollTo({0}, {1});".format(
            scroll_to_x, scroll_to_y))
        x, y = self._scroll_position()
        if (x, y) != (scroll_to_x, scroll_to_y):
            # Probably in the middle of another scroll. Wait and try again.
            if attempts < 10:
                time.sleep(0.1)
                self._scroll_into_view(elem, attempts=attempts + 1)
            else:
                logger.warning("Can't scroll to (%s, %s)", scroll_to_x, scroll_to_y)

        if attempts == 0:
            self.wait_until(lambda *_: self._is_visible(elem))

    def _scroll_center_data(self):
        # http://www.howtocreate.co.uk/tutorials/javascript/browserwindow
        return self.execute_script("""return [window.innerWidth,
                                              window.innerHeight,
                                              document.documentElement.offsetWidth,
                                              document.documentElement.offsetHeight];""")

    def _scroll_position(self):
        return self.execute_script("""return [document.documentElement.scrollTop,
                                              document.documentElement.scrollLeft];""")

    def _is_visible(self, elem):
        # Thanks http://stackoverflow.com/a/15203639/182604
        return self.execute_script("""return (function (el) {
    var rect     = el.getBoundingClientRect(),
        vWidth   = window.innerWidth || doc.documentElement.clientWidth,
        vHeight  = window.innerHeight || doc.documentElement.clientHeight,
        efp      = function (x, y) { return document.elementFromPoint(x, y) };

    // Return false if it's not in the viewport
    if (rect.right < 0 || rect.bottom < 0
            || rect.left > vWidth || rect.top > vHeight)
        return false;

    // Return true if any of its four corners or center are visible
    return (
          el.contains(efp(rect.left,  rect.top))
      ||  el.contains(efp(rect.right, rect.top))
      ||  el.contains(efp(rect.right, rect.bottom))
      ||  el.contains(efp(rect.left,  rect.bottom))
      ||  el.contains(efp(rect.right - rect.width / 2, rect.bottom - rect.height / 2))
    );
})(arguments[0])""", elem)

    def _is_checked(self, elem):
        return elem.get_attribute('checked') == 'true'

    def _set_check_box(self, elem, state):
        if self._is_checked(elem) != state:
            self._scroll_into_view(elem)
            elem.click()

    def _set_select_elem(self, elem, value):
        self._scroll_into_view(elem)
        s = Select(elem)
        s.select_by_value(value)

    def _set_select_elem_by_text(self, elem, text):
        self._scroll_into_view(elem)
        s = Select(elem)
        s.select_by_visible_text(text)

from __future__ import absolute_import, print_function, unicode_literals

import logging
import os.path
import random
import tempfile
import time
from datetime import datetime

from django.conf import settings
from django.core.urlresolvers import reverse
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, NoSuchWindowException, StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select, WebDriverWait
from six import string_types, text_type

from .base import FuncBaseMixin
from .exceptions import SeleniumCantUseElement
from .utils import CommonMixin, get_session_store

logger = logging.getLogger(__name__)


def escape_selenium(text):
    # Selenium seems to do something strange with its page source function:
    #  &quot; gets converted back to "
    #  &#39; gets converted back to '
    # So we need a custom function here, instead of django.utils.html.escape
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


class FuncSeleniumMixin(CommonMixin, FuncBaseMixin):

    @classmethod
    def setUpClass(cls):
        if not cls.display_browser_window():
            cls.__display = Display(visible=False)
            cls.__display.start()
        driver_name = cls.get_driver_name()
        kwargs = cls.get_webdriver_options()
        cls._driver = getattr(webdriver, driver_name)(**kwargs)
        cls._driver.set_page_load_timeout(cls.get_page_load_timeout())
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

    def assertTextPresent(self, text):
        """
        Asserts that the text is present on the current page
        """
        self.assertIn(escape_selenium(text), self._get_page_source())

    def assertTextAbsent(self, text):
        """
        Asserts that the text is not present on the current page
        """
        self.assertNotIn(escape_selenium(text), self._get_page_source())

    def back(self):
        """
        Go back in the browser.
        """
        self._driver.back()

    @property
    def current_url(self):
        """
        The current full URL
        """
        return self._driver.current_url

    def follow_link(self, css_selector):
        """
        Follows the link specified in the CSS selector.
        """
        return self.click(css_selector, wait_for_reload=True)

    def fill(self, fields):
        """
        Fills form inputs using the values in fields, which is a dictionary
        of CSS selectors to values.
        """
        for k, v in fields.items():
            e = self._find_with_timeout(css_selector=k)
            self._fill_input(e, v)

    def fill_by_text(self, fields):
        """
        Same as ``fill`` except the values are text captions. Useful for ``select`` elements.
        """
        for selector, text in fields.items():
            elem = self._find_with_timeout(css_selector=selector)
            self._fill_input_by_text(elem, text)

    def get_url(self, name, *args, **kwargs):
        """
        Gets the named URL, passing *args and **kwargs to Django's URL 'reverse' function.
        """
        kwargs.pop('expect_errors', None)
        self.get_literal_url(reverse(name, args=args, kwargs=kwargs))

    def get_literal_url(self, url, auto_follow=None, expect_errors=None):
        """
        Gets the passed in URL, as a literal relative URL, without using reverse.
        """
        self._get_url_raw(self.live_server_url + url)
        self.wait_until_loaded('body')

    def is_element_present(self, css_selector):
        """
        Returns True if the element specified by the CSS selector is present on the current page,
        False otherwise.
        """
        try:
            self._driver.find_element_by_css_selector(css_selector)
        except NoSuchElementException:
            return False
        return True

    @property
    def is_full_browser_test(self):
        """
        True for Selenium tests, False for WebTest tests.
        """
        return True

    def set_session_data(self, item_dict):
        """
        Set a dictionary of items directly into the Django session.
        """
        # Cookies don't work unless we visit a page first
        if not self._have_visited_page:
            self.get_url('django_functest.emptypage')

        session = self._get_session()
        for name, value in item_dict.items():
            session[name] = text_type(value)
        session.save()

        s2 = self._get_session()
        if all(s2.get(name) == text_type(value) for name, value in item_dict.items()):
            return

        raise RuntimeError("Session not saved correctly")

    def submit(self, css_selector, wait_for_reload=True, auto_follow=None, window_closes=False):
        """
        Submit the form using the input given in the CSS selector
        """
        self.click(css_selector, wait_for_reload=wait_for_reload, window_closes=window_closes)

    def value(self, css_selector):
        """
        Returns the value of the form input specified in the CSS selector
        """
        elem = self._find(css_selector=css_selector)
        if elem.tag_name == 'input' and elem.get_attribute('type') == 'checkbox':
            return self._is_checked(elem)
        elif elem.tag_name == 'input' and elem.get_attribute('type') == 'radio':
            return self._get_radio_button_value(elem)
        else:
            return elem.get_attribute('value')

    # Full browser specific:

    # Configuration methods and attributes
    browser_window_size = None

    display = False  # Display browser window or not?

    default_timeout = 10  # seconds

    driver_name = "Firefox"  # Sensible default, works most places

    page_load_timeout = 20  # seconds

    def get_browser_window_size(self):
        """
        Configuration method: returns the desired browser window height that
        django_functest will attempt to set, as a tuple of (width, height)
        in pixels, or None. Defaults to ``browser_window_size`` attribute.
        """
        return self.browser_window_size

    @classmethod
    def display_browser_window(cls):
        """
        Configuration classmethod: returns a boolean that determines if the browser window
        should be shown, Defaults to ``display`` attribute.
        """
        return cls.display

    @classmethod
    def get_default_timeout(cls):
        """
        Configuration classmethod: returns the time in seconds for Selenium to wait for
        the browser to respond. Default so ``default_timeout`` attribute.
        """
        return cls.default_timeout

    @classmethod
    def get_driver_name(cls):
        """
        Configuration classmethod: returns the driver name i.e. the browser to use.
        Defaults to `driver_name` attribute.
        """
        return cls.driver_name

    @classmethod
    def get_page_load_timeout(cls):
        """
        Configuration classmethod: returns the time in seconds for Selenium to wait
        for the browser to return a page. Defaults to `page_load_timeout` attribute.
        """
        return cls.page_load_timeout

    @classmethod
    def get_webdriver_options(cls):
        """
        Configuration classmethod: returns options to pass to the WebDriver class.
        """
        return {}

    # Runtime methods:

    def click(self, css_selector=None, xpath=None,
              text=None, text_parent_id=None,
              wait_for_reload=False,
              wait_timeout=None,
              double=False, scroll=True, window_closes=False):
        """
        Clicks the button or control specified by the CSS selector
        or xpath
        """
        if window_closes:
            wait_for_reload = False
        if wait_for_reload:
            self._driver.execute_script("document.pageReloadedYetFlag='notyet';")

        elem = self._find_with_timeout(css_selector=css_selector,
                                       xpath=xpath,
                                       text=text,
                                       text_parent_id=text_parent_id,
                                       timeout=wait_timeout)
        if scroll:
            self._scroll_into_view(elem)
        elem.click()
        if double:
            try:
                elem.click()
            except StaleElementReferenceException:
                pass

        if wait_for_reload:
            def f(driver):
                obj = driver.execute_script("return document.pageReloadedYetFlag;")

                if obj is None or obj != "notyet":
                    return True
                return False
            try:
                WebDriverWait(self._driver, self.get_default_timeout()).until(f)
            except NoSuchWindowException:
                # legitimate sometimes e.g. when window closes
                pass
        if not window_closes:
            self._wait_until_finished()

    def execute_script(self, script, *args):
        """
        Executes the suppplied Javascript in the browser and returns the results.
        """
        return self._driver.execute_script(script, *args)

    def hover(self, css_selector):
        """
        Peform a mouse hover over the element specified by the CSS selector.
        """
        elem = self._find(css_selector=css_selector)
        self._scroll_into_view(elem)
        ActionChains(self._driver).move_to_element(elem).perform()

    def is_element_displayed(self, css_selector):
        """
        Returns True if the element specified by the CSS selector is both
        present and visible on the page.
        """
        try:
            elem = self._driver.find_element_by_css_selector(css_selector)
        except NoSuchElementException:
            return False
        return elem.is_displayed()

    def save_screenshot(self, dirname="./", filename=None):
        """
        Saves a screenshot of the browser window.
        """
        # Especially useful when hiding the browser window gives different behaviour.
        testname = '%s.%s.%s' % (self.__class__.__module__, self.__class__.__name__, self._testMethodName)
        if filename is None:
            filename = datetime.now().strftime('Screenshot %Y-%m-%d %H.%M.%S') + " " + testname + ".png"
        name = os.path.abspath(os.path.join(dirname, filename))
        self._driver.save_screenshot(name)
        return name

    def set_window_size(self, width, height):
        """
        Sets the browser window size to specified width and height.
        """
        def f(driver):
            driver.set_window_size(width, height)
            win_width, win_height = self._get_window_size()
            # Some drivers fail to get it exactly
            return ((width - 2 <= win_width <= width + 2) and
                    (height - 2 <= win_height <= height + 2))
        self.wait_until(f)

    def switch_window(self, handle=None):
        """
        Switches window.

        If there are only 2 windows, it can work out which window to switch to.
        Otherwise, you should pass in the window handle as `handle` kwarg.

        Returns a tuple (old_window_handle, new_window_handle)
        """
        try:
            current_window_handle = self._driver.current_window_handle
        except NoSuchWindowException:
            # Window closed recently
            current_window_handle = None
        window_handles = self._driver.window_handles
        if handle is None:
            possible_window_handles = [h for h in window_handles
                                       if h != current_window_handle]

            if len(possible_window_handles) > 1:
                raise AssertionError("Don't know which window to switch to!")
            else:
                handle = possible_window_handles[0]

        def f(driver):
            driver.switch_to_window(handle)
            return driver.current_window_handle == handle
        self.wait_until(f)
        return current_window_handle, handle

    def wait_for_page_load(self):
        """
        Waits until the page has finished loading
        """
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

    def wait_until_loaded(self, css_selector=None, xpath=None,
                          text=None, text_parent_id=None,
                          timeout=None):
        """
        Helper function that blocks until the element with the given tag name
        is found on the page.
        """
        self.wait_until(self._get_finder(css_selector=css_selector, xpath=xpath,
                                         text=text, text_parent_id=text_parent_id),
                        timeout=timeout)

    # Implementation methods - private

    def _get_finder(self, css_selector=None, xpath=None, text=None, text_parent_id=None):
        if css_selector is not None:
            return lambda driver: driver.find_element_by_css_selector(css_selector)
        if xpath is not None:
            return lambda driver: driver.find_element_by_xpath(xpath)
        if text is not None:
            if text_parent_id is not None:
                prefix = '//*[@id="{0}"]'.format(text_parent_id)
            else:
                prefix = ''
            _xpath = prefix + '//*[contains(text(), "{0}")]'.format(text)
            return lambda driver: driver.find_element_by_xpath(_xpath)
        raise AssertionError("No selector passed in")

    def _get_url_raw(self, url):
        """
        'raw' method for getting URL - not compatible between FullBrowserTest and WebTestBase
        """
        self._have_visited_page = True
        self._driver.get(url)

    def _add_cookie(self, cookie_dict):
        self._driver.add_cookie(cookie_dict)

    def _get_session(self):
        session_cookie = self._driver.get_cookie(settings.SESSION_COOKIE_NAME)
        if session_cookie is None:
            # Create new
            session = get_session_store()
            cookie_data = {'name': settings.SESSION_COOKIE_NAME,
                           'value': session.session_key,
                           'path': '/',
                           'secure': False,
                           }
            if self._driver.name == 'phantomjs':
                # Not sure why this is needed, but it seems to do the trick
                cookie_data['domain'] = '.localhost'

            self._add_cookie(cookie_data)
        else:
            session = get_session_store(session_key=session_cookie['value'])
        return session

    def _get_window_size(self):
        if self._driver.name == "phantomjs":
            return self.execute_script("return [document.width, document.height]")
        else:
            return self.execute_script("return [window.outerWidth, window.outerHeight]")

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
        elif elem.tag_name == 'input' and elem.get_attribute('type') == 'radio':
            self._set_radio_button(elem, val)
        elif elem.tag_name == 'input' and elem.get_attribute('type') == 'file':
            # val is an Upload instance
            fname = self._make_temp_file_for_upload(val)
            elem.send_keys(fname)
        else:
            self._scroll_into_view(elem)
            elem.clear()
            elem.send_keys(val)

    def _fill_input_by_text(self, elem, val):
        if elem.tag_name == 'select':
            self._set_select_elem_by_text(elem, val)
        else:
            raise SeleniumCantUseElement("Can't do 'fill_by_text' on elements of type {0}".format(elem.tag_name))

    def _find(self, css_selector=None, xpath=None, text=None, text_parent_id=None):
        return self._get_finder(css_selector=css_selector, xpath=xpath,
                                text=text, text_parent_id=text_parent_id)(self._driver)

    def _find_with_timeout(self, css_selector=None, xpath=None, text=None, text_parent_id=None, timeout=None):
        if timeout != 0:
            self.wait_until_loaded(css_selector=css_selector, xpath=xpath,
                                   text=text, text_parent_id=text_parent_id,
                                   timeout=timeout)
        return self._find(css_selector=css_selector, xpath=xpath,
                          text=text, text_parent_id=text_parent_id)

    def _make_temp_file_for_upload(self, upload):
        fname = os.path.join(tempfile.tempdir,
                             "{0}-{1}".format(random.randint(0, 1000000),
                                              upload.filename))
        with open(fname, "wb") as f:
            f.write(upload.content)

        def rmfile():
            os.unlink(fname)

        self.addCleanup(rmfile)
        return fname

    def _scroll_into_view(self, elem, attempts=0):
        if self._is_center_visible(elem):
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
            self.wait_until(lambda *_: self._is_center_visible(elem))

    def _scroll_center_data(self):
        # http://www.howtocreate.co.uk/tutorials/javascript/browserwindow
        return self.execute_script("""return [window.innerWidth,
                                              window.innerHeight,
                                              document.documentElement.scrollWidth,
                                              document.documentElement.scrollHeight];""")

    def _scroll_position(self):
        return self.execute_script("""return [document.documentElement.scrollTop,
                                              document.documentElement.scrollLeft];""")

    def _is_center_visible(self, elem):
        # Thanks http://stackoverflow.com/a/15203639/182604
        return self.execute_script("""return (function (el) {
    var rect     = el.getBoundingClientRect(),
        vWidth   = window.innerWidth || doc.documentElement.clientWidth,
        vHeight  = window.innerHeight || doc.documentElement.clientHeight,
        efp      = function (x, y) { return document.elementFromPoint(x, y) };

    var e_x = (rect.left + rect.right) / 2;
    var e_y = (rect.top + rect.bottom) / 2;
    // Return false if it's not in the viewport
    if (e_x < 0 || e_y < 0
            || e_x > vWidth || e_y > vHeight)
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

    def _set_radio_button(self, elem, value):
        # The 'elem' found might be one of several (previous Selenium code will have
        # returned the first one that matched, especially if a 'name' selector was
        # used). We need to find the actual one that is has the correct value.
        # We also need to be aware of multiple forms that might be on the page.
        form_elem = elem.find_element_by_xpath("./ancestor::form")
        name = elem.get_attribute('name')
        correct_elem = form_elem.find_element_by_xpath(
            '//input[@type="radio"][@name="{0}"][@value="{1}"]'.format(
                name, value))
        if not self._is_checked(correct_elem):
            self._scroll_into_view(correct_elem)
            correct_elem.click()

    def _get_radio_button_value(self, elem):
        # The 'elem' found might be one of several (previous Selenium code will have
        # returned the first one that matched, especially if a 'name' selector was
        # used). We need to find the actual one that is set.
        form_elem = elem.find_element_by_xpath("./ancestor::form")
        name = elem.get_attribute('name')
        elems = form_elem.find_elements_by_xpath(
            '//input[@type="radio"][@name="{0}"]'.format(name))
        for e in elems:
            if e.get_attribute('checked'):
                return e.get_attribute('value')

    def _set_select_elem(self, elem, value):
        self._scroll_into_view(elem)
        s = Select(elem)
        value = value if isinstance(value, string_types) else str(value)
        s.select_by_value(value)

    def _set_select_elem_by_text(self, elem, text):
        self._scroll_into_view(elem)
        s = Select(elem)
        s.select_by_visible_text(text)

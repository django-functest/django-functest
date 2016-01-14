from .base import FirefoxBase, ChromeBase


# Tests for Selenium specific methods

class TestFuncSeleniumSpecificBase(object):

    def test_is_element_displayed(self):
        self.get_url('admin:login')
        self.assertTrue(self.is_element_displayed('#id_username'))
        self.assertFalse(self.is_element_displayed('#id_something_else'))
        self.execute_script("document.querySelector('#id_username').style.display = 'none';")
        self.assertFalse(self.is_element_displayed('#id_username'))


class TestFuncSeleniumSpecificFirefox(TestFuncSeleniumSpecificBase, FirefoxBase):
    pass


class TestFuncSeleniumSpecificChrome(TestFuncSeleniumSpecificBase, ChromeBase):
    pass

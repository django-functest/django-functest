from .base import ChromeBase, FirefoxBase
from .models import Thing


# Tests for Selenium specific methods

class TestFuncSeleniumSpecificBase(object):

    def setUp(self):
        super(TestFuncSeleniumSpecificBase, self).setUp()
        self.thing = Thing.objects.create(name="Rock",
                                          big=True,
                                          clever=False,
                                          element_type=Thing.ELEMENT_EARTH)

    def test_is_element_displayed(self):
        self.get_url('admin:login')
        self.assertTrue(self.is_element_displayed('#id_username'))
        self.assertFalse(self.is_element_displayed('#id_something_else'))
        self.execute_script("document.querySelector('#id_username').style.display = 'none';")
        self.assertFalse(self.is_element_displayed('#id_username'))

    def test_click(self):
        self.get_url('edit_thing', thing_id=self.thing.id)
        self.click('input[name=check]')
        self.assertTextPresent("Everything is fine")

    def test_click_xpath(self):
        self.get_url('edit_thing', thing_id=self.thing.id)
        self.click(xpath='//input[@name="check"]')
        self.assertTextPresent("Everything is fine")

    def test_double_click(self):
        self.get_url('edit_thing', thing_id=self.thing.id)
        self.click('input[name=check]', double=True)
        self.assertTextPresent("Everything is really fine")


class TestFuncSeleniumSpecificFirefox(TestFuncSeleniumSpecificBase, FirefoxBase):
    pass


class TestFuncSeleniumSpecificChrome(TestFuncSeleniumSpecificBase, ChromeBase):
    pass

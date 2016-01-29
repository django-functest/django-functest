from django.contrib.auth import get_user_model

from django_functest import AdminLoginMixin, ShortcutLoginMixin

from .base import ChromeBase, FirefoxBase, PhantomJSBase, WebTestBase

LOGGED_OUT_URL = "/admin/login/?next=/admin/"


class TestShortcutLoginBase(ShortcutLoginMixin):
    def setUp(self):
        super(TestShortcutLoginBase, self).setUp()
        User = get_user_model()
        self.user = User.objects.create_superuser("admin", "admin@example.com", "password")

    def test_login_succeeds(self):
        self.shortcut_login(username=self.user.username, password="password")
        self.get_url("admin:index")
        self.assertUrlsEqual("/admin/")

    def test_login_raises_exception_with_wrong_password(self):
        self.assertRaises(ValueError, lambda: self.shortcut_login(username=self.user.username, password="foo"))

    def test_logout_succeeds(self):
        self.shortcut_login(username=self.user.username, password="password")
        self.shortcut_logout()
        self.get_url("admin:index")
        self.assertUrlsEqual(LOGGED_OUT_URL)


class TestShortcutLoginWebTest(TestShortcutLoginBase, WebTestBase):
    pass


class TestShortcutLoginFirefox(TestShortcutLoginBase, FirefoxBase):
    pass


class TestShortcutLoginChrome(TestShortcutLoginBase, ChromeBase):
    pass


class TestShortcutLoginPhantomJS(TestShortcutLoginBase, PhantomJSBase):
    pass


class TestAdminLoginBase(AdminLoginMixin):

    def setUp(self):
        super(TestAdminLoginBase, self).setUp()
        User = get_user_model()
        self.user = User.objects.create_superuser("admin", "admin@example.com", "password")

    def test_login_succeeds(self):
        self.do_login(username="admin", password="password", shortcut=False)
        self.get_url("admin:index")
        self.assertUrlsEqual("/admin/")

    def test_login_shortcut_succeeds(self):
        self.do_login(username="admin", password="password", shortcut=True)
        self.get_url("admin:index")
        self.assertUrlsEqual("/admin/")

    def test_login_raises_exception_with_wrong_password(self):
        self.assertRaises(ValueError, lambda: self.do_login(username="admin", password="password_2"))

    def test_logout_succeeds(self):
        self.shortcut_login(username="admin", password="password")
        self.do_logout(shortcut=True)
        self.get_url("admin:index")
        self.assertUrlsEqual(LOGGED_OUT_URL)

    def test_logout_shortcut_succeeds(self):
        self.shortcut_login(username="admin", password="password")
        self.do_logout(shortcut=False)
        self.get_url("admin:index")
        self.assertUrlsEqual(LOGGED_OUT_URL)


class TestAdminLoginWebTest(TestAdminLoginBase, WebTestBase):
    pass


class TestAdminLoginFirefox(TestAdminLoginBase, FirefoxBase):
    pass


class TestAdminLoginChrome(TestAdminLoginBase, ChromeBase):
    pass


class TestAdminLoginPhantomJS(TestAdminLoginBase, PhantomJSBase):
    pass

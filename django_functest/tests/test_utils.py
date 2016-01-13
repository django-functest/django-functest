from django.contrib.auth import get_user_model

from django_functest import ShortcutLoginMixin

from .base import ChromeBase, FirefoxBase, WebTestBase


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


class TestShortcutLoginWebTest(TestShortcutLoginBase, WebTestBase):
    pass


class TestShortcutLoginFirefox(TestShortcutLoginBase, FirefoxBase):
    pass


class TestShortcutLoginChrome(TestShortcutLoginBase, ChromeBase):
    pass

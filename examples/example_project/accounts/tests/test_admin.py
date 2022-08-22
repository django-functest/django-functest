from accounts.tests.base import SeleniumTestBase, WebTestBase

from django_functest import FuncBaseMixin, ShortcutLoginMixin


class UserAdminBase(FuncBaseMixin, ShortcutLoginMixin):
    def test_change_self_details(self):
        import IPython

        IPython.embed()


class UserAdminBaseWT(UserAdminBase, WebTestBase):
    pass


class UserAdminBaseSL(UserAdminBase, SeleniumTestBase):
    pass

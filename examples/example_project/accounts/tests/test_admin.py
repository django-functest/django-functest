from django_functest import FuncBaseMixin, ShortcutLoginMixin

from .base import SeleniumTestBase, WebTestBase
from .factories import create_user


class UserAdminBase(FuncBaseMixin, ShortcutLoginMixin):
    def test_change_self_details(self):
        user = create_user()  # noqa
        ...  # TODO


class UserAdminWT(UserAdminBase, WebTestBase):
    pass


class UserAdminSL(UserAdminBase, SeleniumTestBase):
    pass

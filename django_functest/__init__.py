from __future__ import absolute_import, print_function, unicode_literals

from .base import FuncBaseMixin
from .files import Upload
from .funcselenium import FuncSeleniumMixin
from .funcwebtest import FuncWebTestMixin
from .server import MultiThreadedLiveServerMixin
from .utils import AdminLoginMixin, ShortcutLoginMixin

__version__ = '1.1'

__all__ = ['FuncBaseMixin', 'FuncWebTestMixin', 'FuncSeleniumMixin', 'ShortcutLoginMixin',
           'AdminLoginMixin', 'MultiThreadedLiveServerMixin', 'Upload']


FuncCommonApi = FuncBaseMixin

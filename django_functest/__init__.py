from __future__ import absolute_import, print_function, unicode_literals

from .base import FuncBaseMixin
from .funcselenium import FuncSeleniumMixin
from .funcwebtest import FuncWebTestMixin
from .utils import AdminLoginMixin, ShortcutLoginMixin
from .files import Upload
from .server import MultiThreadedLiveServerMixin

__version__ = '0.2.1'

__all__ = ['FuncBaseMixin', 'FuncWebTestMixin', 'FuncSeleniumMixin', 'ShortcutLoginMixin',
           'AdminLoginMixin', 'MultiThreadedLiveServerMixin', 'Upload']


FuncCommonApi = FuncBaseMixin

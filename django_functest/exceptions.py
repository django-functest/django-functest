from __future__ import absolute_import, print_function, unicode_literals


class WebTestNoSuchElementException(Exception):
    pass


class WebTestMultipleElementsException(Exception):
    pass


class WebTestCantUseElement(Exception):
    pass


class SeleniumCantUseElement(Exception):
    pass

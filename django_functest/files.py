from __future__ import absolute_import, print_function, unicode_literals

from webtest import Upload as WebTestUpload


class Upload(WebTestUpload):
    """"
    A file to upload::

        >>> Upload('filename.txt', b'data')
        <Upload "filename.txt">
    """
    # We deliberately override the docstring of WebTestUpload above,
    # to provide help that works for Selenium too.
    pass

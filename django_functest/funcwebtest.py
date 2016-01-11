from django.core.urlresolvers import reverse
from django_webtest import WebTestMixin


class FuncWebTestMixin(WebTestMixin):

    # Public Common API
    is_full_browser_test = False

    @property
    def current_url(self):
        return self.last_response.request.url

    def get_url(self, name, *args, **kwargs):
        """
        Gets the named URL, passing *args and **kwargs to Django's URL 'reverse' function.
        """
        return self.get_literal_url(reverse(name, args=args, kwargs=kwargs))

    def get_literal_url(self, url):
        """
        Gets the passed in URL, as a literal relative URL, without using reverse.
        """
        return self._get_url_raw(url)

    # Implementation methods - private

    def _get_url_raw(self, url, auto_follow=True, expect_errors=False):
        """
        'raw' method for getting URL - not compatible between FullBrowserTest and WebTestBase
        """
        self.last_response = self.app.get(url, auto_follow=auto_follow, expect_errors=expect_errors)
        return self.last_response

from __future__ import absolute_import, print_function, unicode_literals

import sys

from django.test import testcases

if sys.version_info < (3,):
    import SocketServer as socketserver
else:
    import socketserver


# See
#  https://code.djangoproject.com/ticket/20238
#  https://code.djangoproject.com/ticket/27665
class ThreadedWSGIServer(socketserver.ThreadingMixIn, testcases.WSGIServer):
    pass


class MultiThreadedLiveServerThread(testcases.LiveServerThread):
    def _create_server(self, port):
        return ThreadedWSGIServer((self.host, port),
                                  testcases.QuietWSGIRequestHandler,
                                  allow_reuse_address=False)


class MultiThreadedLiveServerMixin(object):
    """
    Mixin for a LiveServerTestCase to make it multi-threaded.
    """
    @classmethod
    def _create_server_thread(cls, host, possible_ports, connections_override):
        return MultiThreadedLiveServerThread(
            host,
            possible_ports,
            cls.static_handler,
            connections_override=connections_override,
        )

import django
from django.test import testcases

if django.VERSION < (2,):

    try:
        from django.core.servers.basehttp import ThreadedWSGIServer
    except ImportError:
        import socketserver

        # See
        #  https://code.djangoproject.com/ticket/20238
        #  https://code.djangoproject.com/ticket/27665
        class ThreadedWSGIServer(socketserver.ThreadingMixIn, testcases.WSGIServer):
            pass

        class MultiThreadedLiveServerThread(testcases.LiveServerThread):
            if django.VERSION < (1, 11, 2):

                def _create_server(self, port):
                    return ThreadedWSGIServer(
                        (self.host, port),
                        testcases.QuietWSGIRequestHandler,
                        allow_reuse_address=False,
                    )

            else:
                # Django 1.11.2 changed the signature
                def _create_server(self):
                    return ThreadedWSGIServer(
                        (self.host, self.port),
                        testcases.QuietWSGIRequestHandler,
                        allow_reuse_address=False,
                    )

    class MultiThreadedLiveServerMixin:
        """
        Mixin for a LiveServerTestCase to make it multi-threaded.
        """

        if django.VERSION < (1, 11):

            @classmethod
            def _create_server_thread(cls, host, possible_ports, connections_override):
                return MultiThreadedLiveServerThread(
                    host,
                    possible_ports,
                    cls.static_handler,
                    connections_override=connections_override,
                )

        else:
            server_thread_class = MultiThreadedLiveServerThread

else:
    # Django 2.0+ has the behavior we want built in
    class MultiThreadedLiveServerMixin:
        pass

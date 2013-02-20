import time
import traceback


class DoStuff(object):
    """All methods are called AFTER sending data to browser.
    But before connection is closed."""

    PASSWORD = ""
    ALLOW_IP_RANGES = ["128-200.0.0.0-1"]

    def on_access_approved(self, handler):
        """Called when user enters correct password."""
        print "User with {0} has been GRANTED access.".format(
            handler.client_address[0]
        )

    def on_access_deny(self, handler):
        """Called when user was denied from doing stuff
        in the method on_access_approved"""
        print "User with {0} has been DENIED access.".format(
            handler.client_address[0]
        )
        time.sleep(2)  # lets annoy user if it is denied access

    def on_index(self, handler):
        """Called when index page is requested"""
        print "Server sent index page to {0}.".format(
            handler.client_address[0]
        )

    def on_error(self, exception):
        """Called when error occured."""
        traceback.print_exc()

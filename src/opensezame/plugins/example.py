

class DoStuff(object):
    """All methods are called AFTER sending data to browser.
    But before connection is closed."""

    def on_access_approved(self, handler):
        """Called when user enters correct password."""
        print "User has been GRANTED access."

    def on_access_deny(self, handler):
        """Called when user was denied from doing stuff
        in the method on_access_approved"""
        print "User has been DENIED access."

    def on_index(self, handler):
        """Called when index page is requested"""
        print "Server send index page"

    def on_error(self, exception):
        """Called when error occured."""
        print "Error occured."

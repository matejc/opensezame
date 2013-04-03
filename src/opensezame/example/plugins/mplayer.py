
import subprocess
import time
import traceback
import os
import signal


class DoStuff(object):
    """All methods are called AFTER sending data to browser."""

    PASSWORD = ""
    ALLOW_IP_RANGES = []
    fnull = open(os.devnull, "w")
    popen = None

    def on_access_approved(self, handler):
        """Called when user enters correct password."""
        print "User with {0} has been GRANTED access.".format(
            handler.client_address[0]
        )
        value = handler.dcontent.get("value")

        command = handler.dcontent.get("command")
        if command == "start":
            self.popen = subprocess.Popen(
                ["/usr/bin/mplayer", value if value else "http://80.94.69.106:6324/"],
                stdout=self.fnull,
                stderr=self.fnull,
                stdin=self.fnull,
                preexec_fn=os.setsid
            )
            print "command: '{0}' - pid: {1}".format(command, self.popen.pid)
        elif command == "stop":
            if self.popen:
                print "command: '{0}' - killing pid: {1} ...".format(command, self.popen.pid)
                os.killpg(self.popen.pid, signal.SIGTERM)
                self.popen = None
        elif command == "increase":
            subprocess.call(
                ["amixer", "sset", "Master", "{0}%+".format(value if value else '10')],
                stdout=self.fnull,
                stderr=self.fnull,
                stdin=self.fnull,
            )
        elif command == "decrease":
            subprocess.call(
                ["amixer", "sset", "Master", "{0}%-".format(value if value else '10')],
                stdout=self.fnull,
                stderr=self.fnull,
                stdin=self.fnull,
            )
        else:
            print "command: '{0}' - sleeping...".format(command)
            time.sleep(1)

    def on_access_deny(self, handler):
        """Called when user was denied from doing stuff
        in the method on_access_approved"""
        print "User with {0} has been DENIED access.".format(
            handler.client_address[0]
        )

    def on_index(self, handler):
        """Called when index page is requested"""
        print "Server sent index page to {0}.".format(
            handler.client_address[0]
        )

    def on_error(self, exception):
        """Called when error occurred."""
        traceback.print_exc()

    def shutdown(self):
        """Called when opensezame server is shutting down."""
        if self.popen:
            print "terminating pid: {0} ...".format(
                self.popen.pid
            )
            os.killpg(self.popen.pid, signal.SIGTERM)

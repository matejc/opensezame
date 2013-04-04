
from urllib2 import urlopen

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
            try:
                # test if url is valid
                urlopen(value)
            except:
                print "command: '{0}' with value '{1}' is invalid".format(command, value)
            else:
                self.popen = subprocess.Popen(
                    ["/usr/bin/mplayer", value],
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
            try:
                # test if integer is valid
                int(value)
            except:
                print "command: '{0}' with value '{1}' is invalid".format(command, value)
            else:
                subprocess.call(
                    ["amixer", "sset", "Master", "{0}%+".format(value)],
                    stdout=self.fnull,
                    stderr=self.fnull,
                    stdin=self.fnull,
                )

        elif command == "decrease":
            try:
                # test if integer is valid
                int(value)
            except:
                print "command: '{0}' with value '{1}' is invalid".format(command, value)
            else:
                subprocess.call(
                    ["amixer", "sset", "Master", "{0}%-".format(value)],
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

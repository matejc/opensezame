"""
Author: Matej Cotman
"""

from iprange import IPv4Range

import SocketServer
import json
import os
import socket
import ssl
import sys


END_LINE = "\r\n"
END_HEADER = END_LINE * 2


def get_real_path():
    """Returns real path to the file not to the link"""
    abspath = os.path.abspath(__file__)
    if os.path.islink(abspath):
        return os.readlink(abspath)
    else:
        return abspath


def content_length(data):
    nstart = data.find("Content-Length: ") + 16
    nend = data.find(END_LINE, nstart)
    return int(data[nstart:nend])


def decode(data):
    data = data.replace("+", " ")
    result = ""
    i = 0
    while i < len(data):
        if data[i] == "%":
            result += chr(int(data[i + 1:i + 3], 16))
            i += 3
        else:
            result += data[i]
            i += 1
    return result


def content2dict(data):
    data = data[data.find(END_HEADER) + 4:]
    items = data.split("&")
    result = {}
    for item in items:
        parts = item.split("=")
        result[decode(parts[0])] = decode(parts[1])
    return result


def read_file(relative_path):
    return open(os.path.join(prefix, relative_path)).read()


def read_template(plugin, template):
    return read_file(os.path.join("templates", plugin, template))


def ip_in_range(ip, ranges):
    if not ranges:
        return True
    for r in ranges:
        if ip in IPv4Range(r):
            return True
    return False


class MyTCPHandler(SocketServer.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """
    def send_response(self, status_code, htmldata):
        self.request.send(
            "HTTP/1.0 {0} OK{1}Content-Type: "
            "text/html{2}{3}{4}".format(
                status_code, END_LINE, END_HEADER, htmldata, END_LINE
            )
        )
        self.request.close()

    def handle(self):
        try:
            self.request.settimeout(5)
            # self.request is the TCP socket connected to the client
            self.data = self.request.recv(2048)  # , socket.MSG_WAITALL)

            start = self.data.find(' ') + 1
            method = self.data[:start - 1].upper()
            end = self.data.find(' ', start)
            path = self.data[start + 1:end].lower()

            print "request from %s at '/%s' with method '%s'" % (
                self.client_address[0],
                path,
                method
            )

            if path in plugins:

                plugin = plugins[path]

                if method == 'GET':
                    self.request.send(
                        "HTTP/1.0 200 OK{0}Content-Type:"
                        " text/html{1}{2}".format(
                            END_LINE,
                            END_HEADER,
                            read_template(path, "index.html")
                        )
                    )
                    plugin.on_index(self)

                elif method == 'POST':
                    self.dcontent = content2dict(self.data)

                    if plugin.PASSWORD:
                        pass_confirmed = \
                            self.dcontent["passfield"] == plugin.PASSWORD
                    else:
                        pass_confirmed = True

                    in_range = ip_in_range(
                        self.client_address[0],
                        plugin.ALLOW_IP_RANGES
                    )

                    if pass_confirmed and in_range:
                        self.send_response(
                            "200",
                            read_template(path, "done.html")
                        )
                        plugin.on_access_approved(self)
                    else:
                        self.send_response(
                            "401",
                            read_template(path, "deny.html")
                        )
                        plugin.on_access_deny(self)

                else:
                    raise Exception("only GET and POST methods available")

            else:
                raise Exception("url not valid")

        except Exception as ex:
            self.request.sendall(
                "HTTP/1.0 500 Internal Server Error"
                "{0}Content-Type: text/html{1}{2}".format(
                    END_LINE, END_HEADER,
                    "<html><h3 style='color:red'>Error: {0}</h3>"
                    "<pre style='color:red'>{1}</pre></html>".format(
                        ex.__class__.__name__, ex
                    )
                )
            )
            if path in plugins:
                plugins[path].on_error(ex)
        finally:
            self.request.close()


class MyTCPServer(SocketServer.TCPServer):

    def __init__(
            self,
            server_address,
            RequestHandlerClass,
            bind_and_activate=True
    ):
        # See SocketServer.TCPServer.__init__
        # (added ssl-support):
        SocketServer.TCPServer.__init__(
            self, server_address, RequestHandlerClass, False
        )
        if "certfile" in config and "keyfile" in config:
            self.socket = ssl.wrap_socket(
                socket.socket(self.address_family, self.socket_type),
                server_side=True,
                certfile=os.path.join(prefix, config["certfile"]),
                keyfile=os.path.join(prefix, config["keyfile"])
            )
        else:
            self.socket = socket.socket(self.address_family, self.socket_type)

        if bind_and_activate:
            self.server_bind()
            self.server_activate()

    def server_bind(self):
        self.allow_reuse_address = True
        SocketServer.TCPServer.server_bind(self)


def main(prefix_arg=None):
    global prefix, server, config, plugin, plugins

    if prefix_arg:
        prefix = prefix_arg
    else:
        prefix = os.getcwd()

    configpath = os.path.join(prefix, "opensezame.json")
    config = json.load(open(configpath))

    sys.path.append(prefix)

    for p in config["plugins"]:
        plugin = __import__(
            "plugins.{0}".format(p),
            fromlist=['DoStuff']
        ).DoStuff()
        plugins[p] = plugin

    try:
        # Create the server, binding to host address and port
        server = MyTCPServer((config["address"], config["port"]), MyTCPHandler)
        server.serve_forever()
    except KeyboardInterrupt:
        print "\nUser killed the program!"

    finally:
        for plugin in plugins:
            plugins[plugin].shutdown()
        if server is not None:
            server.shutdown()
            server.server_close()
        print "Server killed! ({0})".format(os.getpid())


prefix = None
server = None
config = None
plugin = None
plugins = {}


if __name__ == "__main__":
    main(os.path.dirname(get_real_path()))

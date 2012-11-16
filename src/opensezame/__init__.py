"""
Author: Matej Cotman
"""

import SocketServer
import ssl
import socket
import os
import json
import time


END_LINE = "\r\n"
END_HEADER = END_LINE * 2


def turn_on():
    pass


def turn_off():
    pass


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


prefix = os.path.dirname(get_real_path())
config = json.load(open(os.path.join(prefix, "opensezame.json")))

if config["password"] == "changeme":
    raise Exception("Change the password in 'opensezame.conf' file!")


class MyTCPHandler(SocketServer.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        try:
            self.handle_try()
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
        finally:
            self.request.close()

    def handle_try(self):
        self.request.settimeout(5)
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(2048)  # , socket.MSG_WAITALL)

        start = self.data.find(' ') + 1
        method = self.data[:start - 1].upper()
        end = self.data.find(' ', start)
        path = self.data[start:end].lower()

        print "request is from %s at '%s' with '%s'" % (
            self.client_address[0],
            path,
            method
        )

        if path == '/opensezame':

            if method == 'GET':
                self.request.send(
                    "HTTP/1.0 200 OK{0}Content-Type: text/html{1}{2}".format(
                        END_LINE,
                        END_HEADER,
                        open(config["indexhtml"]).read()
                    )
                )

            elif method == 'POST':
                dcontent = content2dict(self.data)
                if dcontent["dafuckfield"] == config["password"]:
                    htmldata = open(config["donehtml"]).read()
                    turn_on()
                    time.sleep(0.2)
                    turn_off()
                else:
                    htmldata = open(config["denyhtml"]).read()
                    time.sleep(2)

                self.request.send(
                    "HTTP/1.0 200 OK{0}Content-Type: "
                    "text/html{1}{2}".format(
                        END_LINE, END_HEADER, htmldata
                    )
                )
            else:
                raise Exception("only GET and POST methods available")

#        elif path == "/eks/captcha.png":
#            if method == "GET":
#                png_img = open("captcha.png", "rb")
#                self.request.sendall( "HTTP/1.0 200 OK%sContent-Type: image/jpeg%s%s" % (
#                                                                                 END_LINE, END_HEADER,
#                                                                                 png_img.read()
#                                                                                ) )
#                png_img.close()
#            else:
#                raise Exception("only GET for captcha available")

        else:
            raise Exception("url not valid")


class MyTCPServer(SocketServer.TCPServer):

    def __init__(
            self,
            server_address,
            RequestHandlerClass,
            bind_and_activate=True
    ):
        # See SocketServer.TCPServer.__init__
        # (added ssl-support):
        SocketServer.BaseServer.__init__(
            self, server_address, RequestHandlerClass
        )
        self.socket = ssl.wrap_socket(
            socket.socket(self.address_family, self.socket_type),
            server_side=True,
            certfile=os.path.join(prefix, config["certfile"]),
            keyfile=os.path.join(prefix, config["keyfile"])
        )

        if bind_and_activate:
            self.server_bind()
            self.server_activate()

    def server_bind(self):
        self.allow_reuse_address = True
        SocketServer.TCPServer.server_bind(self)

server = None
try:
    # Create the server, binding to host address and port
    server = MyTCPServer((config["address"], config["port"]), MyTCPHandler)
    server.serve_forever()
except KeyboardInterrupt:
    print "\nUser killed the program!"

finally:
    if server is not None:
        server.shutdown()
    print "Server killed!"

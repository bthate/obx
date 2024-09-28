# This file is placed in the Public Domain.


"rest"


import os
import sys
import time


from http.server import HTTPServer, BaseHTTPRequestHandler


from obx         import Object, fmt
from obx.default import Default
from obx.persist import Workdir, fns
from obx.runtime import debug, later, launch


def init():
    "start rest server."
    rest = REST((Config.hostname, int(Config.port)), RESTHandler)
    launch(rest.start)
    debug(f"started rst {fmt(Config)}")
    return rest


def html(txt):
    "return html from text."
    return f"""<!doctype html>
<html>
   {txt}
</html>
"""


class Config(Default): # pylint: disable=R0903

    "Configuration"

    hostname = "localhost"
    port     = 10102


class REST(HTTPServer, Object):

    "REST"

    allow_reuse_address = True
    daemon_thread = True

    def __init__(self, *args, **kwargs):
        HTTPServer.__init__(self, *args, **kwargs)
        Object.__init__(self)
        self.host = args[0]
        self._last = time.time()
        self._starttime = time.time()
        self._status = "start"

    def exit(self):
        "stop server."
        self._status = ""
        time.sleep(0.2)
        self.shutdown()

    def start(self):
        "start server."
        self._status = "ok"
        self.serve_forever()

    def request(self):
        "set time of request."
        self._last = time.time()

    def error(self, _request, addr):
        "handle error."
        exctype, excvalue, _tb = sys.exc_info()
        exc = exctype(excvalue)
        later(exc)
        debug(f'{addr} {excvalue}')


class RESTHandler(BaseHTTPRequestHandler):

    "RequestHandler"

    def setup(self):
        "setup connection."
        BaseHTTPRequestHandler.setup(self)
        self._ip = self.client_address[0]
        self._size = 0

    def send(self, txt):
        "send over the wire."
        self.wfile.write(bytes(txt, "utf-8"))
        self.wfile.flush()

    def write_header(self, htype='text/plain'):
        "respond 200 plus header."
        self.send_response(200)
        self.send_header(f'Content-type {htype}', 'charset=utf-8')
        self.send_header('Server', "1")
        self.end_headers()

    def do_GET(self): # pylint: disable=C0103
        "implement GET."
        if "favicon" in self.path:
            return
        if self.path == "/":
            self.write_header("text/html")
            txt = ""
            for fnm in fns():
                txt += f'<a href="http://{Config.hostname}:{Config.port}/{fnm}">{fnm}</a><br>\n'
            self.send(html(txt.strip()))
            return
        fnm = Workdir.wdr + os.sep + "store" + os.sep + self.path
        try:
            with open(fnm, "r", encoding="utf-8") as file:
                txt = file.read()
                self.write_header("txt/plain")
                self.send(html(txt))
        except (TypeError, FileNotFoundError, IsADirectoryError) as ex:
            self.send_response(404)
            later(ex)
            self.end_headers()

    def log(self, code):
        "log access"
        debug(f'{self.address_string()} {code} {self.path}')

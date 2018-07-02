import io
import shutil
from http.server import BaseHTTPRequestHandler, HTTPServer


class MyHttpHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        r_str = "Hello World"
        enc = 'UTF-8'
        encoded = ''.join(r_str).encode(enc)
        f = io.BytesIO()
        f.write(encoded)
        f.seek(0)
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=%s" % enc)
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        shutil.copyfileobj(f, self.wfile)


httpd = HTTPServer(('', 8080), MyHttpHandler)
#httpd = HTTPServer(('', 8080), BaseHTTPRequestHandler)
print("Server started on 127.0.0.1,port 8080.....")
httpd.serve_forever()
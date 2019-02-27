#!/usr/bin/env python
# Reflects the requests from HTTP methods GET, POST, PUT, and DELETE

from http.server import HTTPServer, BaseHTTPRequestHandler
from optparse import OptionParser
import requests
import gzip

class RequestHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        
        request_path = self.path
        
        print("\n----- Request Start ----->\n")
        print("Request path:", request_path)
        print("Request headers:", self.headers)
        print("<----- Request End -----\n")


        print("sent query to DB")
        
##        r = requests.get("http://localhost:8086/query?db=test3&q=\
##SELECT \"degrees\" \
##FROM \"h2o_temperature\" \
##WHERE time >= 1546329600000ms and time <= 1546329620000ms%0A&epoch=ms")
        influx_url = "http://localhost:8086"+request_path
        r = requests.get(influx_url)
        print("----received data")

        print(r.headers)
        print()
        print(r.content)
        print()
        print("----received data END")


        self.send_response(200)
        for key, value in r.headers.items():
            self.send_header(key,value)
        self.end_headers()
        res = r.content
        gres = gzip.compress(res)
        self.wfile.write(gres)

        
    def do_POST(self):
        
        request_path = self.path
        
        print("\n----- Request Start ----->\n")
        print("Request path:", request_path)
        
        request_headers = self.headers
        content_length = request_headers.get('Content-Length')
        length = int(content_length) if content_length else 0
        
        print("Content Length:", length)
        print("Request headers:", request_headers)
        print("Request payload:", self.rfile.read(length))
        print("<----- Request End -----\n")
        
        self.send_response(200)
        self.end_headers()
    
    do_PUT = do_POST
    do_DELETE = do_GET
        
def main():
    port = 8080
    print('Listening on localhost:%s' % port)
    server = HTTPServer(('', port), RequestHandler)
    server.serve_forever()

        
if __name__ == "__main__":
    parser = OptionParser()
    parser.usage = ("Creates an http-server that will echo out any GET or POST parameters\n"
                    "Run:\n\n"
                    "   reflect")
    (options, args) = parser.parse_args()
    
    main()

# forwarding the query and return it to the grafana
from http.server import HTTPServer, BaseHTTPRequestHandler
from optparse import OptionParser
import requests
import gzip
import json
import math
import timeit


class RequestHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        doGet_start = timeit.default_timer()
        request_path = self.path
        
##        print("\n----- Request Start ----->\n")
##        print("Request path:", request_path)
##        print("Request headers:", self.headers)
##        print("<----- Request End -----\n")
##        print("sent query to DB")
        
        influx_url = "http://localhost:8086"+request_path
        print(influx_url)
##        print(influx_url)        
##        print("----received data END")

        start = timeit.default_timer()
        r = requests.get(influx_url)
        stop = timeit.default_timer()
        print('Query Time: ', stop - start) 


##        print("----received data")
##        print("r.header")
##        print(r.headers)      
##        print("####################")
        
        self.send_response(200)
        for key, value in r.headers.items():
            self.send_header(key,value)
        self.end_headers()

        res = r.content
        gres = gzip.compress(res)
        self.wfile.write(gres)           
##        print("----received data END")
        doGet_end = timeit.default_timer()
        print("doGet Time: ",doGet_end-doGet_start)
        
 
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

from http.server import HTTPServer, BaseHTTPRequestHandler
from optparse import OptionParser
import urllib.parse as up
import requests
import gzip
import json
import math
import QueryInfo as qi


class RequestHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        
        request_path = self.path
        
        print("\n----- Request Start ----->\n")
        print("Request path:", request_path)
        print("Request headers:", self.headers)
        print("<----- Request End -----\n")
        
        influx_url = "http://localhost:8086"+request_path
        urlquery = up.urlparse(influx_url).query
        tuple_list = up.parse_qsl(urlquery)
        query_string = tuple_list[-1][1]
        

##        influx_url = "http://localhost:8086/query?db=test&epoch=ms&q=SELECT+%22degrees%22+FROM+%22h2o_temperature%22+WHERE+time+%3E%3D+1546329600000ms+and+time+%3C%3D+1546329620000ms"
        
        
 #       r = requests.get(influx_url)

        ## COUNT THE DATA
        q = request_path.split('+')
        q[1] = ('count%28%2A%29')
        count = '+'.join(q)
        count_url = "http://localhost:8086"+count
        count_query = requests.get(count_url)
        jdict = json.loads(count_query.content)
        count = jdict["results"][0]["series"][0]["values"][0][1]

        print("COUNT", jdict["results"][0]["series"][0]["values"][0][1])


        max_point = 2000
        if count <= max_point:
            print("DIDN'T MODIFY THE QUERY")
            r = requests.get(influx_url)
        else:
            query_info = qi.QueryInfo(query_string)
            lowerlimit = query_info.get_time_range()[0]
            upperlimit = query_info.get_time_range()[1]
            print(lowerlimit, upperlimit)
            

            groupsize = math.floor((upperlimit-lowerlimit)/max_point)
            print(groupsize)

            new_query = query_info.add_group_by(groupsize)
            print(new_query)

            new_tuple =("q",new_query)
            tuple_list[-1] = new_tuple

            parturl = up.urlencode(tuple_list)
            new_url = "http://localhost:8086/query?"+parturl
            print("QUERY MODIFIED, NEW QUERY IS : ")
            print(new_url)
##            end_index = influx_url.find("q=")+2
##            new_query = influx_url[:end_index]+q_url

            r = requests.get(new_url)
        
        print("----received data")
        print("r.header")
        print(r.headers)
        print()
        
        json_dict = json.loads(r.content)
        print("####################")
        #print(json_dict)
        #print("data")
        #print(json_dict["results"][0]["series"][0]["values"])
        
        data = json_dict["results"][0]["series"][0]["values"]
        print("LENGTH OF DATA RECEIVED ",len(data))
        

        self.send_response(200)
        for key, value in r.headers.items():
            self.send_header(key,value)
        self.end_headers()

        res = r.content
        gres = gzip.compress(res)
        self.wfile.write(gres)
 


        
##        
##        if count <= 100:
##            res = r.content
##            gres = gzip.compress(res)
## 
##        else:
##            batchsize = math.floor(count/100)
##            newlist = []
##            for i in range(0,len(data),batchsize):
##                newlist.append(data[i])
##
##            print("SIZE OF THE NEW LIST ",len(newlist))
##
##            json_dict["results"][0]["series"][0]["values"] = newlist
##
##            string_dict = json.dumps(json_dict)
##            byte_dict = string_dict.encode()
##                
##            gres = gzip.compress(byte_dict)
##
##        self.wfile.write(gres)
            
                
                
            
        print("----received data END")


        
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
    #port = 8910
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
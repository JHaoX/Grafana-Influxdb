import requests
import json
import numpy

from tslearn.piecewise import SymbolicAggregateApproximation
from tslearn.utils import to_time_series

from tslearn.preprocessing import TimeSeriesScalerMeanVariance

def main():
    influx_url = "http://localhost:8086/query?db=test_quarter&epoch=ms&q=SELECT+%22degrees%22+FROM+%22h2o_temperature%22+WHERE+time+%3E%3D+1546329600000ms+and+time+%3C%3D+1546329650000ms"
    r = requests.get(influx_url)
    json_dict = json.loads(r.content)

    data = json_dict["results"][0]["series"][0]["values"]
    print(data)

    
    lst2 = [item[1] for item in data]
    n_segments = len(lst2)
    ts = to_time_series(lst2)
    
    alphabet_size_avg = 20
    sax = SymbolicAggregateApproximation(n_segments, alphabet_size_avg)
    scalar = TimeSeriesScalerMeanVariance(mu=0., std=1.)
    sdb = scalar.fit_transform(lst2)
    sax_data = sax.transform(sdb)
 #   sax_data = sax.inverse_transform(sax.fit_transfrom(lst2))
    print(sax_data.shape)
    print(sax_data)
    
    
    

##    print(r.headers)
##    print(r.content)

    

main()

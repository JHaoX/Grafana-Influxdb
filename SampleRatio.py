import requests
import json
import numpy
import matplotlib.pyplot as plt

from tslearn.piecewise import SymbolicAggregateApproximation
from tslearn.utils import to_time_series

from tslearn.preprocessing import TimeSeriesScalerMeanVariance
from tslearn.preprocessing import TimeSeriesResampler


def main():
    influx_url = "http://localhost:8086/query?db=test_quarter&epoch=ms&q=SELECT+%22degrees%22+FROM+%22h2o_temperature%22+WHERE+time+%3E%3D+1546329600000ms+and+time+%3C%3D+1546329650000ms"
    r = requests.get(influx_url)
    json_dict = json.loads(r.content)

    data = json_dict["results"][0]["series"][0]["values"]
    print(data)
   
    lst2 = [item[1] for item in data]
    n_segments = len(lst2)
    alphabet_size_avg = 20

    sax = SymbolicAggregateApproximation(n_segments, alphabet_size_avg)
    scalar = TimeSeriesScalerMeanVariance(mu=0., std=1.)
    
    sdb = scalar.fit_transform(lst2)
    sax_data = sax.transform(sdb)
    print(sax_data.shape)
    print(sax_data)

##    sample_fill_url = "http://localhost:8086/query?db=test_quarter&epoch=ms&q=SELECT+sample%28%22degrees%22%2C10%29+FROM+%22h2o_temperature%22+WHERE+time+%3E%3D+1546329600000ms+and+time+%3C%3D+1546329650000ms+GROUP+BY+time(1s)+fill(linear)"
    sample_url = "http://localhost:8086/query?db=test_quarter&epoch=ms&q=SELECT+sample%28%22degrees%22%2C10%29+FROM+%22h2o_temperature%22+WHERE+time+%3E%3D+1546329600000ms+and+time+%3C%3D+1546329650000ms"
    r2 = requests.get(sample_url)
    json_dict2 = json.loads(r2.content)
    sampled_data = json_dict2["results"][0]["series"][0]["values"]
    print(sampled_data)
   
    sample = [item[1] for item in sampled_data]
    print(sample)

    start_x = data[0][0]

    end_x = data[-1][0]
    current_x = start_x
    current_loc = 0
    slope = (sampled_data[current_loc][1]-sampled_data[current_loc+1][1])/(sampled_data[current_loc][0] - sampled_data[current_loc+1][0])
    intersection = sampled_data[current_loc][1]-slope*sampled_data[current_loc][0]
    
    sample_fit = []
    while current_x <= end_x:
        if current_x>=sampled_data[current_loc+1][0] and current_loc+1 < len(sampled_data)-2:
            print(current_x, current_loc)
            current_loc+=1
            slope = (sampled_data[current_loc][1]-sampled_data[current_loc+1][1])/(sampled_data[current_loc][0] - sampled_data[current_loc+1][0])
            intersection = sampled_data[current_loc][1]-slope*sampled_data[current_loc][0]
        
        sample_fit.append([current_x, slope*current_x+intersection])
        current_x += 1000 #1000ms

    print(sample_fit)
    

            
            
        
        
        

##    sdb2 = scalar.fit_transform(TimeSeriesResampler(sz=len(lst2)).fit_transform(sample))
##    sdb2 = scalar.fit_transform(sample)
##    sax_sample = sax.transform(sdb2)

##    print(sax_sample.shape)
##    print(sax_sample)
##    
##    print("distance")
##    print(sax.distance(sax_data, sax_sample))
##
    plt.figure()
    plt.subplot(2,2,1)
    x = [item[0] for item in sample_fit]
    y = [item[1] for item in sample_fit]
##    plt.plot(sdb[0].ravel(),'b-')
    plt.plot(x,y,'bo-')
   
##    plt.plot(sample,'r-')
    plt.title("raw data")

    plt.subplot(2,2,2)
##    plt.plot(sdb2[0].ravel(),'bo')
    x = [item[0] for item in sampled_data]
    y = [item[1] for item in sampled_data]
    plt.plot(x,y,'bo-')
    plt.title("sample data")
##    
    plt.tight_layout()
    plt.show()
    
    


main()

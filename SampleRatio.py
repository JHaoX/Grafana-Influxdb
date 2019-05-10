import requests
import json
import numpy
import matplotlib.pyplot as plt
import math

from tslearn.piecewise import SymbolicAggregateApproximation
from tslearn.utils import to_time_series

from tslearn.preprocessing import TimeSeriesScalerMeanVariance
from tslearn.preprocessing import TimeSeriesResampler


##dbname = "NOAA_water_database"
dbname = "test_quarter"

def main():
# fetch original data
    #for test_quarter db
    influx_url = "http://localhost:8086/query?db=" + dbname + \
                 "&epoch=ms&q=SELECT+%22degrees%22+FROM+%22h2o_temperature%22+WHERE+time+%3E%3D+1546329600000ms+and+time+%3C%3D+1546329900000ms"

    #FOR NOAA DB
##    influx_url = "http://localhost:8086/query?db=" + dbname + \
##                 "&epoch=ms&q=SELECT+%22degrees%22+FROM+%22h2o_temperature%22+WHERE+time+%3E%3D+1439856000000ms+and+time+%3C%3D+1439992520000ms+and%28%22location%22+%3D+%27santa_monica%27%29"
    
    r = requests.get(influx_url)
    json_dict = json.loads(r.content)

    data = json_dict["results"][0]["series"][0]["values"]
    print(data[0])
    print(data[1])
    time_interval = data[1][0] - data[0][0] # consistant time interval
    print("time interval: ", time_interval)
   
    lst2 = [item[1] for item in data]
    n_segments = len(lst2)
    
    print("original data size", len(lst2))
    alphabet_size_avg = 20

    sax = SymbolicAggregateApproximation(n_segments, alphabet_size_avg)
    scalar = TimeSeriesScalerMeanVariance(mu=0., std=1.)
    
    sdb = scalar.fit_transform(lst2)
    sax_data = sax.transform(sdb)
#    print(sax_data)
    s3 = sax.fit_transform(sax_data)
    print("s3")
 #   print(s3)

# generate sample data
    sample_size = 50
    sample_url = "http://localhost:8086/query?db="+dbname+\
                 "&epoch=ms&q=SELECT+sample%28%22degrees%22%2C" + str(sample_size) +\
                 "%29+FROM+%22h2o_temperature%22+WHERE+time+%3E%3D+1546329600000ms+and+time+%3C%3D+1546329900000ms"

##    sample_url = "http://localhost:8086/query?db=" + dbname + \
##                 "&epoch=ms&q=SELECT+sample%28%22degrees%22%2C" + str(sample_size) +\
##                 "%29+FROM+%22h2o_temperature%22+WHERE+time+%3E%3D+1439856000000ms+and+time+%3C%3D+1442612520000ms+and%28%22location%22+%3D+%27santa_monica%27%29"

    
    r2 = requests.get(sample_url)
    json_dict2 = json.loads(r2.content)
    sampled_data = json_dict2["results"][0]["series"][0]["values"] # [[time, value], ...]

    print("sample length")
    print(len(sampled_data))
   
    sample = [item[1] for item in sampled_data] #[value,...]
   # print(sample)
    

    start_x = data[0][0]
    end_x = data[-1][0]
    current_x = start_x
    current_loc = 0
    
    slope = (sampled_data[current_loc][1]-sampled_data[current_loc+1][1])\
            /(sampled_data[current_loc][0] - sampled_data[current_loc+1][0])
    intersection = sampled_data[current_loc][1]-slope*sampled_data[current_loc][0]

    sample_fit = []
    
    while current_x <= end_x:
        #print(current_x)
        ## if current x
        if current_x>=sampled_data[current_loc+1][0] and current_loc+1 < len(sampled_data)-1:
            current_loc+=1
            slope = (sampled_data[current_loc] [1]-sampled_data[current_loc+1][1]) \
                    /(sampled_data[current_loc][0] - sampled_data[current_loc+1][0])
            intersection = sampled_data[current_loc][1] - slope*sampled_data[current_loc][0]
        
        sample_fit.append([current_x, slope*current_x+intersection])
        current_x += time_interval #1000ms
    
    print("sample_fit")
    print(sample_fit[0])  #sampled data
    print(sample_fit[1])

    sample_fit_extract = [item[1] for item in sample_fit]
    fit_sample_data = scalar.fit_transform(sample_fit_extract)
 
    sax_sample_data = sax.transform(fit_sample_data)
    s4 = sax.fit_transform(sax_sample_data)
    print("distance")
    dist = sax.distance_sax(s3[0], s4[0])
    print(dist)
    print("normalized distance")
    print(dist/math.sqrt(sample_size))
    
    

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
    plt.plot(x,y,'bo-')
    plt.ylim(top = 82, bottom = 58)
    plt.title("sample data (linear fill)")

    plt.subplot(2,2,2)
##    plt.plot(sdb2[0].ravel(),'bo')
    x = [item[0] for item in sampled_data]
    y = [item[1] for item in sampled_data]
    plt.plot(x,y,'bo-')
    plt.title("sample data")
##
    plt.subplot(2,2,3)
    plt.plot(lst2,'bo-')
    plt.title("original dataset")

    plt.tight_layout()
    plt.show()
##    
    
main()

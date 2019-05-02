import random
import math

print("# DDL")

print("CREATE DATABASE sinedb")

print("# DML")

print("# CONTEXT-DATABASE: sinedb")

for i in range(1546300800, 1546948800):
	print("h2o_temperature,location=santa_monica degrees={} {}".format(10*math.sin(i/10000) + random.randint(-3,3),i))



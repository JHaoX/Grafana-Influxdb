import random
print("# DDL")

print("CREATE DATABASE test3")

print("# DML")

print("# CONTEXT-DATABASE: test3")


for i in range(1546300800, 1546948800):
	print("h2o_temperature,location=santa_monica degrees={} {}".format(random.randint(60,80),i))



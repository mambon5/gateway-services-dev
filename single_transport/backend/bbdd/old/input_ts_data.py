#!/usr/bin/python

# time series data, use influxDB

from influxdb import InfluxDBClient

# create an influxDBClient instance (server)
client = InfluxDBClient(host='localhost', port=8086)

# create db
client.create_database('time_series_example')
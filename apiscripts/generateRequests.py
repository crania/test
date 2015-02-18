__author__ = 'drager'
import requests
import random
i = 1
while i < 10000:
    i = i + 1
    response = requests.get(
        url='http://192.168.59.103:5000/hit/' + str(i))


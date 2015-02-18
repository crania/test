__author__ = 'drager'


import json
import requests
import random
import time

pages = ['finding the needed money to buy a car','why the cloud is turning dark','help us raise the roof','obama said something at some place','there is always another page']
sections = ['headlines','home','tips for success','latest','archive']
referrers = ['facebook.com','google.com','linkedin.com','twitter.com','fark.com']
base_demo_url = 'http://192.168.59.103:5000/'

content = dict(top_article = 'Mom arrested for too much sugar', top_ad = 'Greate makup advice by MakeCo')

for i in range(1226,1000000):
    putdata = { 'referrer' : referrers[random.randrange(0,4)], 'section' : sections[random.randrange(0,4)], 'tagsf' : ['asdf','fda'], 'content' : content}
    response = requests.put(
        url='http://192.168.59.103:5000/hit/' + pages[random.randrange(0,4)] + '?hit_id=' + str(i),
        data = json.dumps(putdata))
    time.sleep(1)
    print i
print response.text
            #data=json.dumps(tv))
        #logging.info(response.text)


content = dict(top_article = 'Mom arrested for too much sugar', top_ad = 'Greate makup advice by MakeCo')
data = json.dumps({'page_name' : 'home', 'referrer' : 'facebook.com', 'content' : content})

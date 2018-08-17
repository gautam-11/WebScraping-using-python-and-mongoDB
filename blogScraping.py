import requests
from bs4 import BeautifulSoup
from csv import writer
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017')
db = client.blog
collection = db.posts
res = requests.get('http://codedemos.com/sampleblog/')

soup = BeautifulSoup(res.text, 'html.parser')
posts = soup.find_all(class_ = 'post-preview')

for post in posts:
    title = post.find(class_='post-title').get_text().replace('\n','')
    link = post.find('a')['href']
    date = post.select('.post-date')[0].get_text()
    bson = {
        'title':title,
        'link':link,
        'date':date
    }
    res = collection.insert_one(bson)
    print('Inserted document = {}'.format(res.inserted_id))

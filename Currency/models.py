from django.db import models

# Create your models here.
class NewsModel:
    def __init__(self,title,img,desc,media,link,date):
        self.title = title
        self.image = img
        self.description = desc
        self.media = media
        self.link = link
        self.date = date
from django.db import models
from django.db.models.base import Model
from django.contrib.auth.models import User
from datetime import datetime
from PIL import Image
# Create your models here.

class Blog(models.Model):
    title = models.TextField(max_length=100)
    content = models.TextField(max_length=500)
    image = models.ImageField(null=True,default="media/blogindex.jpg",upload_to="blog-pics")
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    date = models.DateTimeField(default=datetime.now)
    slug = models.CharField(max_length=100,default=None,null=True)
    def __str__(self):
        return f'{self.title} by {self.user_id.username}'

    def save(self,*args,**kwargs):
        if len(self.content) > 20:
            self.slug=self.content[:20]
        else:
            self.slug = self.content
        super().save(*args,**kwargs)
        img = Image.open(self.image)

        if img.height > 1000 or img.width > 1000:
            output = (800,800)
            img.thumbnail(output)
            img.save(self.image.path)

        


class Comment(models.Model):
    comment_text = models.TextField(max_length=100) 
    blog_id = models.ForeignKey(Blog,on_delete=models.CASCADE)
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    date = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f'{self.comment_text} by {self.user_id.username}'
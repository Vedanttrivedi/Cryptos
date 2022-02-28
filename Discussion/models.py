from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from PIL import Image

class DisQuestion(models.Model):
    title = models.TextField(max_length=100,null=False)
    user_id = models.ForeignKey(User,on_delete=models.CASCADE,null=False)
    date = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f'{self.title} started by {self.user_id.username}'

class DisAnswer(models.Model):
    question_id = models.ForeignKey(DisQuestion,on_delete=models.CASCADE,null=False)
    user_id = models.ForeignKey(User,on_delete=models.CASCADE,null=False)
    image = models.ImageField(default="media/answer.jpg",upload_to="media/discussion-pics",null=True)
    body = models.TextField(max_length=500)
    date = models.DateTimeField(default=datetime.now)
    vote_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.body} by {self.user_id.username}"

    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)
        img = Image.open(self.image.path)
         
        if img.height > 1000 or img.width > 1000:
            output = (800,800)
            img.thumbnail(output)
            img.save(self.image.path)
        
        

class UpVotes(models.Model):
    like = models.ManyToManyField(User)
    answer = models.ForeignKey(DisAnswer,on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.answer} "s" total likes {self.like.count()}'
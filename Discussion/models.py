from django.db import models
from django.contrib.auth.models import User
from blog.models import Blog
from datetime import datetime



class DisQuestion(models.Model):
    title = models.TextField(max_length=100,null=False)
    user_id = models.ForeignKey(User,on_delete=models.CASCADE,null=False)
    date = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f'{self.title} started by {self.user_id.username}'

class DisAnswer(models.Model):
    question_id = models.ForeignKey(DisQuestion,on_delete=models.CASCADE,null=False)
    user_id = models.ForeignKey(User,on_delete=models.CASCADE,null=False)
    image = models.ImageField(default="models/answer.jpg",upload_to="media/DisCussion",null=True)
    body = models.TextField(max_length=500)
    date = models.DateTimeField(default=datetime.now)


    def __str__(self):
        return "f{self.body} by {self.user_id.username}"
from django.contrib import admin
from . models import DisQuestion,DisAnswer,UpVotes
# Register your models here.
admin.site.register(DisQuestion)
admin.site.register(DisAnswer)
admin.site.register(UpVotes)
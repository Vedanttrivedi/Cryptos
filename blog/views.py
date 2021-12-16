from django.shortcuts import render

# Create your views here.

def blogList(request):
    return render(request,"blog/blog.html")
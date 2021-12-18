from django.contrib import messages
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from . models import Blog, Comment
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# Create your views here.

def blogList(request):
    blogs = Blog.objects.all().order_by('-date')
    return render(request,"blog/blogList.html",{"blogs":blogs})

@login_required
def blogCreate(request):
    if request.method=="POST":
        title = request.POST["title"]
        content = request.POST["content"]
        if "image" in request.FILES.keys():
            print(request.FILES["image"])
            img = request.FILES["image"]
            if str(img).endswith(".jpg") or str(img).endswith(".png") or str(img).endswith(".jpeg"):
                blg = Blog(title=title,content=content,user_id=request.user,image=img)
            else:
                messages.info(request,"Invalid image format..supported formats=[jpg,png,jpeg]")
                return redirect("blogCreatePage")
        else:
            blg = Blog(title=title,content=content,user_id=request.user)
        blg.save()
        messages.info(request,"Blog Posted")
        return redirect(f'/blog/{blg.id}')
    return render(request,"blog/blogCreate.html")

@login_required
def oneBlog(request,id):
    try:
        blog = Blog.objects.get(id=id)
        comments = Comment.objects.filter(blog_id=blog).order_by('-date')
        context = {"blog":blog,"comments":comments}
        return render(request,"blog/oneBlog.html",context)
    except Exception as e:
        return HttpResponse(str(e))


@login_required
def comment(request):
    if request.method=="POST":
        try:
            blogid = request.POST["blogid"]
            blog = Blog.objects.get(id=blogid)
            text = request.POST["text"]
            comm = Comment(comment_text=text,blog_id=blog,user_id=request.user)
            comm.save()
            messages.info(request,"Comment Posted")
            return redirect(f'/blog/{blog.id}')
        except Exception as e:
            messages.info(request,"something went wrong try again")
            return HttpResponse(e)
        
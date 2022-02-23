from django.contrib import messages
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from blog.models import Blog
from . models import DisQuestion,DisAnswer,UpVotes
from django.contrib.auth.decorators import login_required

def discussionList(request):
    questions = DisQuestion.objects.all().order_by('-date')
    return render(request,"Discussion/discussionList.html",{"questions":questions})


@login_required
def discussionCreate(request):
    if request.method=="POST":
        title = request.POST["title"]
        if "image" in request.FILES.keys():
            print(request.FILES["image"])
            img = request.FILES["image"]
            if str(img).endswith(".jpg") or str(img).endswith(".png") or str(img).endswith(".jpeg"):
                dis = DisQuestion(title=title,user_id=request.user,image=img)
            else:
                messages.info(request,"Invalid image format..supported formats=[jpg,png,jpeg]")
                return redirect("discussionCreatePage")
        else:
            dis = DisQuestion(title=title,user_id=request.user)
        dis.save()
        messages.info(request,"Question Posted")
        return redirect(f'/discussion/{dis.id}')
    return render(request,"Discussion/discussionCreate.html")

@login_required
def oneDiscussion(request,id):
    try:
        question = DisQuestion.objects.get(id=id)
        answers = DisAnswer.objects.filter(question_id=question).order_by('-date')
        context = {"question":question,"answers":answers}
        return render(request,"Discussion/oneQuestion.html",context)
    except Exception as e:
        return HttpResponse(str(e))

@login_required
def answer(request):
    if request.method=="POST":
        questionid = int(request.POST["questionid"])
        question = DisQuestion.objects.get(id=questionid)
        text = request.POST["text"]
        if "image" in request.FILES.keys():
            images = request.FILES["image"]
            if str(images).endswith(".jpg") or  str(images).endswith(".png") or  str(images).endswith(".jpeg"):
                answer = DisAnswer(body=text,question_id=question,user_id=request.user,image=images)
                answer.save()
            else:
                messages.info(request,"Invalid image format..supported formats=[jpg,png,jpeg]")
                return redirect(f'/discussion/{question.id}')
            
        else:
            answer = DisAnswer(body=text,question_id=question,user_id=request.user)
            answer.save()
        messages.info(request,"Answer Posted")
        return redirect(f'/discussion/{question.id}')
    return redirect(f'/discussion/')


@login_required
def likeAnswer(request):
    if request.method=="POST":
        ansid = int(request.POST["ansid"])
        disans = DisAnswer.objects.get(id=ansid)
        upvote = UpVotes.objects.get(id=disans.id)
        count = 0
        if request.user in upvote.like.all():
            upvote.like.remove(request.user)
            upvote.save()
            count = upvote.like.count()
        else:
            upvote.like.add(request.user)
            count = upvote.like.count()
        return HttpResponse(count)

from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.discussionList,name="discussionListPage"),
    path('create/',views.discussionCreate,name="discussionCreatePage"),
    path('<int:id>/',views.oneDiscussion,name="oneDiscussionPage"),
    path('answer/',views.answer,name="answerPage"),
    path('likeAnswer/',views.likeAnswer,name="likeAnswerPage"),
]
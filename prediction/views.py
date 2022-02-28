from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required
def predict(request):
    return render(request,'prediction/predict.html')
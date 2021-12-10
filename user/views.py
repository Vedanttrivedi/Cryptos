from django.shortcuts import render, resolve_url,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
# Create your views here.

def home(request):
    return render(request,'user/base.html')
    
def login(request):
    if request.method=="POST":
        name = request.POST["username"]
        password =make_password( request.POST["password"])
        user = User.objects.filter(username=name,password=password)
        user1 =  User.objects.filter(email=name,password=password)
        if  user is not None:
            login(request,user)
            return HttpResponse(f"{user.username}")
        elif  user1 is not None:
            login(request,user1)
            return HttpResponse(f"{user1.username}")
        if True:
            return redirect("/user/login")
    return render(request,"user/login.html")



def register(request):
    if request.method=="POST":
        firstname = request.POST["firstname"]
        lastname = request.POST["lastname"]
        username = request.POST["username"]
        email = request.POST["email"]
        password = make_password(request.POST["password"])
        conpassword = make_password(request.POST["conpassword"])
        user=  User(first_name=firstname,last_name=lastname,email=email,password=password,username=username)
        user.is_active = True
        user.save()
        return redirect("/user/login")
    return render(request,"user/register.html")



def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "user/password/password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Cryptos',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect ("/password_reset/done/")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="user/password/password_reset.html", context={"password_reset_form":password_reset_form})
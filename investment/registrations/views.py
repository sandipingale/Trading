from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .forms import CreateUserform
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout, get_user_model
import json

from django.conf import settings
from django.core.mail import send_mail
from .token import account_activation_token
from django.utils.encoding import force_text
from django.contrib import messages
from .decorators import unauthenticated_user

# Create your views here.

@unauthenticated_user
def register_user(request):
    form = CreateUserform()
    context = {}
    errors = []
    context['form'] = form
    if request.method == 'POST':
        form = CreateUserform(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string('registrations/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            messages.success(request,"Accouns added successfully, please check your email for activations link")
            return render(request, 'registrations/register.html', {})


    e_list = json.loads(form.errors.as_json())
    print(e_list)
    for fields in e_list:
        for er in e_list[fields]:
            errors.append(er["message"])
    context["errors"] = errors
    return render(request, 'registrations/register.html', context)

@unauthenticated_user
def login_user(request):
    errors = []
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        print(form)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                request.session['groups'] = [x.name for x in request.user.groups.all()]
                request.session.modified = True
                return redirect('home')
            else:
                print("Error ins logging in user")
        else:
            print("Error ins logging in")
    else:
        form = AuthenticationForm()

    e_list = json.loads(form.errors.as_json())
    for fields in e_list:
        for er in e_list[fields]:
            errors.append(er["message"])

    return render(request, 'registrations/login.html', {'errors': errors})

def logout_user(request):
    logout(request)
    return redirect('login')

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request,'Thank you for your email confirmation. Now you can login your account.')
        return redirect('/accounts/login')
    else:
        messages.error(request,'Activation Links is invalid')
        return redirect('/accounts/login')
        
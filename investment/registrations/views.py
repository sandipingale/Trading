from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.models import User

from .forms import CreateUserform
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout, get_user_model
import json

from django.conf import settings
from django.core.mail import send_mail
from .token import account_activation_token
from django.utils.encoding import force_str
from django.contrib import messages
from .decorators import unauthenticated_user
from django.contrib.auth.models import Group

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
            check_user_on_email = User.objects.filter(email=user.email)
            if check_user_on_email:
                context["errors"] = ["Email already in use"]
                return render(request, 'registrations/register.html', context)
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
        print(request.POST.get('username'))
        if '@' in request.POST.get('username'):
            tmp_email = request.POST.get('username')
            check_user_on_email = User.objects.filter(email=tmp_email)
            if check_user_on_email:
                username = check_user_on_email[0].username
                request.POST._mutable=True
                request.POST['username'] = username
                request.POST._mutable=False
        form = AuthenticationForm(request, data=request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None and user.is_active:
                logout(request)
                #login(request, user)
            if user is not None:
                login(request, user)
                request.session['groups'] = [x.name for x in request.user.groups.all()]
                request.session.modified = True
                return redirect('home')
            else:
                print("Error in logging in user")
        else:
            print("Erro ins logging in")
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
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        group = Group.objects.get(name='test_group')
        user.groups.add(group)
        user.save()
        messages.success(request,'Thank you for your email confirmation. Now you can login your account.')
        return redirect('/accounts/login')
    else:
        messages.error(request,'Activation Links is invalid')
        return redirect('/accounts/login')
        
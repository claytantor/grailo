# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from django.utils import simplejson
import random
from feeds.forms import RegisterForm
from django.shortcuts import redirect
from django.contrib.auth.models import User
from feeds.models import Templar
import uuid
from django.core.exceptions import ObjectDoesNotExist

def index(request):
    context = {}
    return render(request, 'index.html', context)

def home(request):
    if request.user.is_authenticated():
        context = {}
        return render(request, 'home.html', context)
    else:
        context = {}
        return render(request, 'login.html', context)

def login_user(request):
    view = 'error.html'
    context = {'message':'UNKNOWN ERROR'}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                # Redirect to a success page.
                return redirect('home.html', foo='bar')
            else:
            # Return a 'disabled account' error message
                context['message']=request.POST['username']+' account has been suspended.'
        else:
            context['message']=request.POST['username']+' account was not found.'
    else:
        context['message']='GET not supported.'

    return render(request, view, context)

def logout_user(request):
    logout(request)
    return redirect('index.html', foo='bar')

def register(request):
    model = {}
    if request.method == 'POST': # If the form has been submitted...
        form = RegisterForm(request.POST)
        if form.is_valid():
            clean_data = form.cleaned_data
            user = \
                User.objects.create_user(
                    clean_data['handel'], None, clean_data['pw_unencrypted'])
            templar =\
                Templar.objects.create(
                    public_key = clean_data['public_key'],
                    avatar = clean_data['avatar_img'],
                    pw_encrypted=clean_data['pw_encrypted'],
                    user = user
                )

            return redirect('home.html', foo='bar')
        else:
            model['form'] = form
            return render(request, 'register.html', model)
    else:
        model['form'] = RegisterForm()
        return render(request, 'register.html', model)

def uname_json(request):

    context = {}

    if request.GET.get('uname',None):
        try:
            templar = Templar.objects.get(user__username=request.GET['uname'])
            context['uname']=templar.user.username
            context['pw_encrypted']=templar.pw_encrypted
            context['avatar_img']=templar.avatar
            context['public_key']=templar.public_key
        except ObjectDoesNotExist:
            print ''
            context['error']='USER NOT FOUND'
            context['message']=request.GET['uname']+' is not a valid Grailo user.'

    else:
        f = open('/Users/claygraham/data/github/grailo/static/data/words_small.txt', 'r')

        lines = []
        while 1:
            line = f.readline()
            lines.append(line.replace('\n','').lower())
            if not line:
                break
            pass # do something

        uuid_user = str(uuid.uuid4())

        #print lines
        l1 = len(lines)-1
        index = random.randint(0,len(lines)-1)
        number = random.randint(0,100)
        uname = lines[index]+str(number)
        context['uname']=uname
        context['uuid']=uuid_user

    data = simplejson.dumps(context)
    return HttpResponse(data, mimetype='application/json')


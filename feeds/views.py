# Create your views here.

import uuid
import random
import re
import cStringIO
from datetime import datetime
from PIL import Image

from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from django.utils import simplejson
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.urlresolvers import reverse


from models import Message, FeedFollowers, Templar,Feed
from forms import MessageForm,RegisterForm,FeedForm

if "notification" in settings.INSTALLED_APPS:
    from notification import models as notification
else:
    notification = None

def index(request,
          template_name="index.html"):
    return render_to_response(template_name, {
    }, context_instance=RequestContext(request))

@login_required
def home(request,
         template_name="home.html"):

    return render_to_response(template_name, {
        }, context_instance=RequestContext(request))

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
                return redirect(request.POST['next'],foo='bar')
            else:
            # Return a 'disabled account' error message
                context['message']=request.POST['username']+' account has been suspended.'
        else:
            context['message']=request.POST['username']+' account was not found.'
    else:
        #http://localhost:8000/feeds/login.html?next=/feeds/home.html
        context['next']=request.GET['next']
        view = 'login.html'

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
        f = open(settings.GRAILO_USER_WORDS, 'r')

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

def profile_detail(request, username, template_name="profile.html"):
    return render_to_response(template_name, {
        "username": username
    }, context_instance=RequestContext(request))

@login_required
def templar_feeds(request, form_class=FeedForm,
                  template_name="feeds.html", success_url=None):
    templar = Templar.objects.get(user=request.user)

    if request.method == "POST": #save new feed
        form = form_class(templar,request.POST)
        if form.is_valid():
            form.save()
            if success_url is None:
                success_url = reverse('feeds.views.templar_feeds')
                return HttpResponseRedirect(success_url)
    else:
        form = form_class(templar)

    feeds = Feed.objects.filter(owner=templar)
    return render_to_response(template_name, {
        'feeds': feeds,
        'form':form,
    }, context_instance=RequestContext(request))



def feed(request, feed_id, form_class=MessageForm,
                template_name="feed.html", success_url=None):
    if request.method == "POST": #save new message
        feed =  get_object_or_404(Feed, id=feed_id)
        templar = Templar.objects.get(user=request.user)
        form = form_class(feed,templar,request.POST)
        if form.is_valid():
            form.save()
            if success_url is None:
                success_url = reverse('feeds.views.feed',args=(feed_id,) )
                return HttpResponseRedirect(success_url)
    else: #get feed by id
        feed = get_object_or_404(Feed, id=feed_id)
        form = form_class(feed)

    return render_to_response(template_name, {
        "form": form,
        "feed":feed
    }, context_instance=RequestContext(request))

@login_required
def message(request, message_id,
                template_name="message.html", success_url=None):

    message = get_object_or_404(Message, id=message_id)
    return render_to_response(template_name, {
        "message": message
    }, context_instance=RequestContext(request))

def avatar_png(request, uname):
    templar = Templar.objects.get(user__username=uname)
    datauri = templar.avatar
    imgstr = re.search(r'base64,(.*)', datauri).group(1)
    tempimg = cStringIO.StringIO(imgstr.decode('base64'))
    img = Image.open(tempimg)
    response = HttpResponse(mimetype="image/png")
    img.save(response, "PNG")
    return response




#@login_required
#def personal(request, form_class=MessageForm,
#             template_name="personal.html", success_url=None):
#    """
#    just the messages the current user is following
#    """
#    #grailo_account = grailo_account_for_user(request.user)
#    twitter_authorized = None
#
#    if request.method == "POST":
#        form = form_class(request.user, request.POST)
#        if form.is_valid():
#            text = form.cleaned_data['text']
#            form.save()
#            if success_url is None:
#                success_url = reverse('feeds.views.personal')
#            return HttpResponseRedirect(success_url)
#        reply = None
#    else:
#        reply = request.GET.get("reply", None)
#        form = form_class()
#        if reply:
#            form.fields['text'].initial = u"@%s " % reply
#    messages = MessageInstance.objects.messages_for(request.user).order_by("-sent")
#    return render_to_response(template_name, {
#        "form": form,
#        "reply": reply,
#        "messages": messages,
#        "twitter_authorized": False,
#        }, context_instance=RequestContext(request))
#
#
#def public(request, template_name="public.html"):
#    """
#    all the messages
#    """
#    messages = Message.objects.all().order_by("-sent")
#
#    return render_to_response(template_name, {
#        "messages": messages,
#        }, context_instance=RequestContext(request))
#
#def single(request, id, template_name="single.html"):
#    """
#    A single message.
#    """
#    message = get_object_or_404(Message, id=id)
#    return render_to_response(template_name, {
#        "message": message,
#        }, context_instance=RequestContext(request))
#
#
#def _follow_list(request, other_user, follow_list, template_name):
#    # the only difference between followers/following views is template
#    # this function captures the similarity
#
#    return render_to_response(template_name, {
#        "other_user": other_user,
#        "follow_list": follow_list,
#        }, context_instance=RequestContext(request))
#
#def followers(request, username, template_name="followers.html"):
#    """
#    a list of users following the given user.
#    """
#    other_user = get_object_or_404(User, username=username)
#    users_followers = Following.objects.filter(followed_object_id=other_user.id, followed_content_type=ContentType.objects.get_for_model(other_user))
#    follow_list = [u.follower_content_object for u in users_followers]
#    return _follow_list(request, other_user, follow_list, template_name)
#
#def following(request, username, template_name="following.html"):
#    """
#    a list of users the given user is following.
#    """
#    other_user = get_object_or_404(User, username=username)
#    following = Following.objects.filter(follower_object_id=other_user.id, follower_content_type=ContentType.objects.get_for_model(other_user))
#    follow_list = [u.followed_content_object for u in following]
#    return _follow_list(request, other_user, follow_list, template_name)
#
#def toggle_follow(request, username):
#    """
#    Either follow or unfollow a user.
#    """
#    other_user = get_object_or_404(User, username=username)
#    if request.user == other_user:
#        is_me = True
#    else:
#        is_me = False
#    if request.user.is_authenticated() and request.method == "GET" and not is_me:
#        if request.GET["action"] == "follow":
#            Following.objects.follow(request.user, other_user)
#            #request.user.message_set.create(message=_("You are now following %(other_user)s") % {'other_user': other_user})
#            #if notification:
#            #    notification.send([other_user], "message_follow", {"user": request.user})
#        elif request.GET["action"] == "unfollow":
#            Following.objects.unfollow(request.user, other_user)
##            request.user.message_set.create(message=_("You have stopped following %(other_user)s") % {'other_user': other_user})
#
#    return HttpResponseRedirect(reverse("profile_detail", args=[other_user]))


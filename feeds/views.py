# Create your views here.

import uuid
import random
import re
import cStringIO
from PIL import Image

from django.forms.models import model_to_dict
from django.http import HttpResponse
from django.http import Http404
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
from django.middleware import csrf


from models import Message, FeedFollowers, Templar,Feed
from forms import MessageForm,RegisterForm,FeedForm


def index(request,
          template_name="index.html"):
    return render_to_response(template_name, {
    }, context_instance=RequestContext(request))

@login_required
def home(request,
         template_name="home.html"):

    templar = Templar.objects.get(user=request.user)
    feeds = Feed.objects.filter(owner=templar)

    followed_feeds_id_list = FeedFollowers.objects.filter(
        follower = templar
    ).values_list('feed',flat=True)

    followed_feeds = Feed.objects.filter(id__in=followed_feeds_id_list)

    return render_to_response(template_name, {
        'feeds':feeds,
        'followed_feeds':followed_feeds
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

    templar = Templar.objects.get(user__username=username)

    if not templar:
        raise Http404

    feeds = Feed.objects.filter(owner=templar)

    #following feeds
    followed_feeds_id_list = FeedFollowers.objects.filter(
        follower = templar
    ).values_list('feed',flat=True)

    followed_feeds = Feed.objects.filter(id__in=followed_feeds_id_list)

    return render_to_response(template_name, {
        'templar': templar,
        'feeds':feeds,
        'followed_feeds':followed_feeds
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

    follow_feed = None
    if request.user.is_authenticated():
        templar = Templar.objects.get(user=request.user)
    else :
        templar = None

    feed =  get_object_or_404(Feed, id=feed_id)
    followers_id_list = FeedFollowers.objects.filter(
        feed = feed
    ).values_list('follower',flat=True)

    #followersfollowed_feeds = Feed.objects.filter(id__in=followed_feeds_id_list)
    following_templars = Templar.objects.filter(id__in=followers_id_list)

    if request.method == "POST": #save new message

        form = form_class(feed, None, templar, request.POST)

        if form.is_valid():
            form.save()
            if success_url is None:
                success_url = reverse('feeds.views.feed',args=(feed_id,) )
                return HttpResponseRedirect(success_url)

    else: #get feed by id
        form = form_class(feed)

    #if authentcated
    if templar:
        try:
            follow_feed = FeedFollowers.objects.get(
                feed = feed,
                follower = templar
            )
        except ObjectDoesNotExist:
            follow_feed = None

    #figure out messages
    all_messages = []
    messages = Message.objects.filter(feed=feed, reply_to=None)
    for message in messages:
        dict_message = model_to_dict(message)
        templar = Templar.objects.get(id=message.templar.id)
        dict_message['templar'] = templar
        dict_message['indent'] = 0
        #recurse
        all_messages.append(dict_message)

    return render_to_response(template_name, {
        "form": form,
        "feed":feed,
        "messages":messages,
        "csrf_token_native":csrf.get_token(request),
        "follow_feed":follow_feed,
        "followers":following_templars,
    }, context_instance=RequestContext(request))

@login_required
def follow_feed(request, feed_id):
    context={}
    if request.method == "GET":
        feed =  get_object_or_404(Feed, id=feed_id)
        templar = Templar.objects.get(user=request.user)
        if request.GET.get("toggle","on") == "on":
            #make the relation
            follow_relation = FeedFollowers.objects.create(
                feed = feed,
                follower = templar
            )
            follow_relation.save()
            context['status']="SUCCEED"
            context['state']="on"
        else:
            follow_relation = FeedFollowers.objects.filter(
                feed = feed,
                follower = templar
            )
            follow_relation.all().delete()
            context['status']="SUCCEED"
            context['state']="off"

    data = simplejson.dumps(context)
    return HttpResponse(data, mimetype='application/json')

@login_required
def message(request, message_id,
                template_name="message.html", success_url=None):

    message = get_object_or_404(Message, id=message_id)
    return render_to_response(template_name, {
        "message": message
    }, context_instance=RequestContext(request))

@login_required
def reply_message(request, message_id, form_class=MessageForm,
                  template_name="feed.html", success_url=None):
    templar = Templar.objects.get(user=request.user)
    messageReplyTo = get_object_or_404(Message, id=message_id)

    if request.method == "POST": #save new message
        form = form_class(messageReplyTo.feed,messageReplyTo,templar,request.POST)
        if form.is_valid():
            form.saveReply(messageReplyTo)
            success_url = reverse('feeds.views.feed',args=(messageReplyTo.feed.id,) )
            return HttpResponseRedirect(success_url)
        else:
            return feed(request,messageReplyTo.feed.id)
    else:
        form=form_class()
        return feed(request,messageReplyTo.feed.id)

@login_required
def delete_message(request, message_id, form_class=MessageForm,
                   template_name="feed.html", success_url=None):
    message_delete = get_object_or_404(Message, id=message_id)
    feed_id =  message_delete.feed.id
    message_delete.delete()
    return feed(request,feed_id)

def avatar_png(request, uname):
    templar = Templar.objects.get(user__username=uname)
    datauri = templar.avatar
    imgstr = re.search(r'base64,(.*)', datauri).group(1)
    tempimg = cStringIO.StringIO(imgstr.decode('base64'))
    img = Image.open(tempimg)
    response = HttpResponse(mimetype="image/png")
    img.save(response, "PNG")
    return response



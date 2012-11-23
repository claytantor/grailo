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

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from feeds.utils import grailo_account_for_user, grailo_verify_credentials
from feeds.models import Message, MessageInstance, Following
from feeds.forms import MessageForm


if "notification" in settings.INSTALLED_APPS:
    from notification import models as notification
else:
    notification = None

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

def personal(request, form_class=MessageForm,
             template_name="microblogging/personal.html", success_url=None):
    """
    just the messages the current user is following
    """
    grailo_account = grailo_account_for_user(request.user)

    if request.method == "POST":
        form = form_class(request.user, request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            form.save()
            if request.POST.get("pub2grailo", False):
                grailo_account.PostUpdate(text)
            if success_url is None:
                success_url = reverse('microblogging.views.personal')
            return HttpResponseRedirect(success_url)
        reply = None
    else:
        reply = request.GET.get("reply", None)
        form = form_class()
        if reply:
            form.fields['text'].initial = u"@%s " % reply
    messages = MessageInstance.objects.messages_for(request.user).order_by("-sent")
    return render_to_response(template_name, {
        "form": form,
        "reply": reply,
        "messages": messages,
        "grailo_authorized": grailo_verify_credentials(grailo_account),
        }, context_instance=RequestContext(request))
personal = login_required(personal)

def public(request, template_name="microblogging/public.html"):
    """
    all the messages
    """
    messages = Message.objects.all().order_by("-sent")

    return render_to_response(template_name, {
        "messages": messages,
        }, context_instance=RequestContext(request))

def single(request, id, template_name="microblogging/single.html"):
    """
    A single message.
    """
    message = get_object_or_404(Message, id=id)
    return render_to_response(template_name, {
        "message": message,
        }, context_instance=RequestContext(request))


def _follow_list(request, other_user, follow_list, template_name):
    # the only difference between followers/following views is template
    # this function captures the similarity

    return render_to_response(template_name, {
        "other_user": other_user,
        "follow_list": follow_list,
        }, context_instance=RequestContext(request))

def followers(request, username, template_name="microblogging/followers.html"):
    """
    a list of users following the given user.
    """
    other_user = get_object_or_404(User, username=username)
    users_followers = Following.objects.filter(followed_object_id=other_user.id, followed_content_type=ContentType.objects.get_for_model(other_user))
    follow_list = [u.follower_content_object for u in users_followers]
    return _follow_list(request, other_user, follow_list, template_name)

def following(request, username, template_name="microblogging/following.html"):
    """
    a list of users the given user is following.
    """
    other_user = get_object_or_404(User, username=username)
    following = Following.objects.filter(follower_object_id=other_user.id, follower_content_type=ContentType.objects.get_for_model(other_user))
    follow_list = [u.followed_content_object for u in following]
    return _follow_list(request, other_user, follow_list, template_name)

def toggle_follow(request, username):
    """
    Either follow or unfollow a user.
    """
    other_user = get_object_or_404(User, username=username)
    if request.user == other_user:
        is_me = True
    else:
        is_me = False
    if request.user.is_authenticated() and request.method == "POST" and not is_me:
        if request.POST["action"] == "follow":
            Following.objects.follow(request.user, other_user)
            request.user.message_set.create(message=_("You are now following %(other_user)s") % {'other_user': other_user})
            if notification:
                notification.send([other_user], "message_follow", {"user": request.user})
        elif request.POST["action"] == "unfollow":
            Following.objects.unfollow(request.user, other_user)
            request.user.message_set.create(message=_("You have stopped following %(other_user)s") % {'other_user': other_user})
    return HttpResponseRedirect(reverse("profile_detail", args=[other_user]))


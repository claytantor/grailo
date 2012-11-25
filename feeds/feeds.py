from atompub.atom import Feed
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from models import Message, MessageInstance
from templatetags.microblogging_tags import render_message_text
from django.template.defaultfilters import linebreaks, capfirst
from datetime import datetime

ITEMS_PER_FEED = getattr(settings, 'PINAX_ITEMS_PER_FEED', 20)

class BaseMessageFeed(Feed):
    def item_id(self, message):
        return "http://%s%s#%s" % (
            Site.objects.get_current().domain,
            reverse('feeds.views.single', args=[message.id,]),
            message.id,
            )

    def item_title(self, message):
        return message.text

    def item_updated(self, message):
        return message.sent

    def item_published(self, message):
        return message.sent

    def item_content(self, message):
        return {"type" : "html", }, linebreaks(render_message_text(message))

    def item_links(self, message):
        return [{"href" : self.item_id(message)}]

    def item_authors(self, message):
        return [{"name" : message.sender.username}]


class MessageFeedAll(BaseMessageFeed):
    def feed_id(self):
        return 'http://%s/feeds/messages/all/' % Site.objects.get_current().domain

    def feed_title(self):
        return 'Messages Feed for all users'

    def feed_updated(self):
        qs = Message.objects.all()
        # We return an arbitrary date if there are no results, because there
        # must be a feed_updated field as per the Atom specifications, however
        # there is no real data to go by, and an arbitrary date can be static.
        if qs.count() == 0:
            return datetime(year=2008, month=7, day=1)
        return qs.latest('sent').sent

    def feed_links(self):
        absolute_url = reverse('profiles.views.profiles')
        complete_url = "http://%s%s" % (
            Site.objects.get_current().domain,
            absolute_url,
            )
        return ({'href': complete_url},)

    def items(self):
        return Message.objects.order_by("-sent")[:ITEMS_PER_FEED]


class MessageFeedUser(BaseMessageFeed):
    def get_object(self, params):
        return get_object_or_404(User, username=params[0].lower())

    def feed_id(self, user):
        return 'http://%s/feeds/messages/only/%s/' % (
            Site.objects.get_current().domain,
            user.username,
            )

    def feed_title(self, user):
        return 'Messages Feed for User %s' % capfirst(user.username)

    def feed_updated(self, user):
        qs = Message.objects.filter(sender_id=user.id, sender_type=ContentType.objects.get_for_model(user))
        # We return an arbitrary date if there are no results, because there
        # must be a feed_updated field as per the Atom specifications, however
        # there is no real data to go by, and an arbitrary date can be static.
        if qs.count() == 0:
            return datetime(year=2008, month=7, day=1)
        return qs.latest('sent').sent

    def feed_links(self, user):
        absolute_url = reverse('profiles.views.profile', args=[user.username,])
        complete_url = "http://%s%s" % (
            Site.objects.get_current().domain,
            absolute_url,
            )
        return ({'href': complete_url},)

    def items(self, user):
        return Message.objects.filter(sender_id=user.id, sender_type=ContentType.objects.get_for_model(user)).order_by("-sent")[:ITEMS_PER_FEED]


class MessageFeedUserWithFriends(BaseMessageFeed):
    def get_object(self, params):
        return get_object_or_404(User, username=params[0].lower())

    def feed_id(self, user):
        return 'http://%s/feeds/messages/with_friends/%s/' % (
            Site.objects.get_current().domain,
            user.username,
            )

    def feed_title(self, user):
        return 'Messages Feed for User %s and friends' % capfirst(user.username)

    def feed_updated(self, user):
        qs = MessageInstance.objects.messages_for(user)
        # We return an arbitrary date if there are no results, because there
        # must be a feed_updated field as per the Atom specifications, however
        # there is no real data to go by, and an arbitrary date can be static.
        if qs.count() == 0:
            return datetime(year=2008, month=7, day=1)
        return qs.latest('sent').sent

    def feed_links(self, user):
        absolute_url = reverse('profiles.views.profile', args=[user.username,])
        complete_url = "http://%s%s" % (
            Site.objects.get_current().domain,
            absolute_url,
            )
        return ({'href': complete_url},)

    def items(self, user):
        return MessageInstance.objects.messages_for(user).order_by("-sent")[:ITEMS_PER_FEED]

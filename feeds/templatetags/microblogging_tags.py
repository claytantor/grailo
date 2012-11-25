import re

from django import template
from django.core.urlresolvers import reverse
from django.template.defaultfilters import stringfilter
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.contrib.contenttypes.models import ContentType
from feeds.models import Message


register = template.Library()
user_ref_re = re.compile("@(\w+)")


def make_user_link(text):
    username = text.group(1)
    return """@<a href="%s">%s</a>""" % (reverse("profile_detail", args=[username]), username)


@register.simple_tag
def render_message_text(message):
    text = escape(message.text)
    text = user_ref_re.sub(make_user_link, text)
    return mark_safe(text)


@register.inclusion_tag('listing.html', takes_context=True)
def message_listing(context, messages, prefix_sender, are_mine):
    request = context.get('request', None)
    sc = {
        'messages': messages.select_related(depth=1),
        'prefix_sender': prefix_sender,
        'are_mine': are_mine
    }
    if request is not None:
        sc['request'] = request
    return sc


@register.inclusion_tag('listing.html', takes_context=True)
def sent_message_listing(context, user, prefix_sender, are_mine):
    messages = Message.objects.filter(sender_id=user.pk)
    return message_listing(context, messages, prefix_sender, are_mine)


#@register.simple_tag
#def follower_count(user):
#    followers = Following.objects.filter(
#        followed_object_id = user.id,
#        followed_content_type = ContentType.objects.get_for_model(user)
#    )
#    return followers.count()
#
#
#@register.simple_tag
#def following_count(user):
#    following = Following.objects.filter(
#        follower_object_id = user.id,
#        follower_content_type = ContentType.objects.get_for_model(user)
#    )
#    return following.count()

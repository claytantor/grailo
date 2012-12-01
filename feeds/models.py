from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils.translation import ugettext_lazy as _


# relational databases are a terrible way to do
# multicast messages (just ask Twitter) but here you have it :-)
import re
reply_re = re.compile("^@(\w+)")

class Templar(models.Model):
    user = models.ForeignKey(User)
    public_key = models.CharField(max_length=250, unique=True)
    get_absolute_url = models.CharField(max_length=250)
    pw_encrypted = models.TextField()
    avatar = models.TextField()

class Feed(models.Model):
    title = models.CharField(max_length=250)
    public_key = models.CharField(max_length=250)
    created = models.DateTimeField(_('created'), default=datetime.now)

    #relationships
    owner = models.ForeignKey(Templar, related_name='feeds',null=True, blank=True)
    followers = models.ManyToManyField(
        'Templar',
        through='FeedFollowers',
        blank=True, null=True)

class Message(models.Model):
    feed = models.ForeignKey(Feed,null=True, related_name='messages', blank=True)
    templar = models.ForeignKey(Templar, related_name='messages',null=True, blank=True)
    reply_to = models.ForeignKey('Message', related_name='replies', null=True, blank=True)
    text = models.CharField(max_length=250)
    sent = models.DateTimeField(_('sent'), default=datetime.now)

class FeedFollowers(models.Model):
    feed = models.ForeignKey(Feed,null=True,blank=True)
    follower = models.ForeignKey('Templar',null=True,blank=True)
    def __unicode__(self):
        return self.feed.name+' '+self.follower.user.username



#class Message(models.Model):
#    """
#    a single message from a user
#    """
#
#    text = models.CharField(_('text'), max_length=140)
#    sender_type = models.ForeignKey(ContentType)
#    sender_id = models.PositiveIntegerField()
#    sender = generic.GenericForeignKey('sender_type', 'sender_id')
#    sent = models.DateTimeField(_('sent'), default=datetime.now)
#
#    def __unicode__(self):
#        return self.text
#
#    def get_absolute_url(self):
#        return ("single_message", [self.id])
#    get_absolute_url = models.permalink(get_absolute_url)
#
#    class Meta:
#        ordering = ('-sent',)
#
#
#class MessageInstanceManager(models.Manager):
#
#    def messages_for(self, recipient):
#        recipient_type = ContentType.objects.get_for_model(recipient)
#        return MessageInstance.objects.filter(recipient_type=recipient_type, recipient_id=recipient.id)
#
#
#class MessageInstance(models.Model):
#    """
#    the appearance of a message in a follower's timeline
#
#    denormalized for better performance
#    """
#
#    text = models.CharField(_('text'), max_length=140)
#    sender_type = models.ForeignKey(ContentType, related_name='message_instances')
#    sender_id = models.PositiveIntegerField()
#    sender = generic.GenericForeignKey('sender_type', 'sender_id')
#    sent = models.DateTimeField(_('sent'))
#
#    # to migrate to generic foreign key, find out the content_type id of User and do something like:
#    # ALTER TABLE "microblogging_messageinstance"
#    #     ADD COLUMN "recipient_type_id" integer NOT NULL
#    #     REFERENCES "django_content_type" ("id")
#    #     DEFAULT <user content type id>;
#    #
#    # NOTE: you will also need to drop the foreign key constraint if it exists
#
#    # recipient = models.ForeignKey(User, related_name="received_message_instances", verbose_name=_('recipient'))
#
#    recipient_type = models.ForeignKey(ContentType)
#    recipient_id = models.PositiveIntegerField()
#    recipient = generic.GenericForeignKey('recipient_type', 'recipient_id')
#
#    objects = MessageInstanceManager()
#
#
#def message(sender, instance, created, **kwargs):
#    #if message is None:
#    #    message = Message.objects.create(text=text, sender=user)
#    recipients = set() # keep track of who's received it
#    user = instance.sender
#
#    # add the sender's followers
#    user_content_type = ContentType.objects.get_for_model(user)
#    followings = Following.objects.filter(followed_content_type=user_content_type, followed_object_id=user.id)
#    for follower in (following.follower_content_object for following in followings):
#        recipients.add(follower)
#
#    # add sender
#    recipients.add(user)
#
#    # if starts with @user send it to them too even if not following
#    match = reply_re.match(instance.text)
#    if match:
#        try:
#            reply_recipient = User.objects.get(username=match.group(1))
#            recipients.add(reply_recipient)
#        except User.DoesNotExist:
#            pass # oh well
#        else:
#            if notification:
#                notification.send([reply_recipient], "message_reply_received", {'message': instance,})
#
#    # now send to all the recipients
#    for recipient in recipients:
#        message_instance = MessageInstance.objects.create(text=instance.text, sender=user, recipient=recipient, sent=instance.sent)
#
#
#class FollowingManager(models.Manager):
#
#    def is_following(self, follower, followed):
#        try:
#            following = self.get(follower_object_id=follower.id, followed_object_id=followed.id)
#            return True
#        except Following.DoesNotExist:
#            return False
#
#    def follow(self, follower, followed):
#        if follower != followed and not self.is_following(follower, followed):
#            Following(follower_content_object=follower, followed_content_object=followed).save()
#
#    def unfollow(self, follower, followed):
#        try:
#            following = self.get(follower_object_id=follower.id, followed_object_id=followed.id)
#            following.delete()
#        except Following.DoesNotExist:
#            pass
#
#
#class Following(models.Model):
#    follower_content_type = models.ForeignKey(ContentType, related_name="followed", verbose_name=_('follower'))
#    follower_object_id = models.PositiveIntegerField()
#    follower_content_object = generic.GenericForeignKey('follower_content_type', 'follower_object_id')
#
#    followed_content_type = models.ForeignKey(ContentType, related_name="followers", verbose_name=_('followed'))
#    followed_object_id = models.PositiveIntegerField()
#    followed_content_object = generic.GenericForeignKey('followed_content_type', 'followed_object_id')
#
#    objects = FollowingManager()
#
#post_save.connect(message, sender=Message)


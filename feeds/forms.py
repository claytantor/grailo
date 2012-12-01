from django import forms
from models import Message,Feed

#try:
#    from notification import models as notification
#except ImportError:
#    notification = None

class RegisterForm(forms.Form):
    handel = forms.CharField(max_length=32,widget=forms.HiddenInput())
    public_key = forms.CharField(max_length=250,widget=forms.HiddenInput())
    pw_encrypted = forms.CharField(max_length=512,widget=forms.HiddenInput())
    pw_unencrypted = forms.CharField(max_length=128,widget=forms.HiddenInput())
    avatar_img = forms.CharField(max_length=20000,widget=forms.HiddenInput())

class FeedForm(forms.ModelForm):
    title = forms.CharField(
        label='Feed Title',
        max_length=250,
        widget=forms.TextInput(attrs={
            'placeholder':'Name of the new feed.',
            'class':'fld_title_feed',
        }))
    public_key = forms.CharField(max_length=250,required=False,widget=forms.HiddenInput())

    class Meta:
        model = Feed
        exclude = ('followers', 'created')

    def __init__(self, owner= None, *args, **kwargs):
        self.owner = owner
        super(FeedForm, self).__init__(*args, **kwargs)

    def save(self):
        feed_instance = super(FeedForm, self).save(commit=False)
        feed_instance.title = self.cleaned_data["title"]
        feed_instance.public_key = self.cleaned_data["public_key"]
        feed_instance.owner = self.owner
        feed_instance.save()

class MessageForm(forms.ModelForm):

    #encrypted
    text = forms.CharField(max_length=512,widget=forms.HiddenInput())

    class Meta:
        model = Message
        exclude = ('sent')

    def __init__(self, feed=None, reply_to=None, templar=None, *args, **kwargs):
        self.feed = feed
        self.reply_to=reply_to
        self.templar = templar
        super(MessageForm, self).__init__(*args, **kwargs)

    def clean_text(self):
        return self.cleaned_data['text'].strip()

    def saveReply(self,reply_to):
        text = self.cleaned_data["text"]
        message_instance = super(MessageForm, self).save(commit=False)
        message_instance.feed = self.feed

        message_instance.reply_to = reply_to
        message_instance.templar = self.templar

        message_instance.save()

    def save(self):
        text = self.cleaned_data["text"]
        message_instance = super(MessageForm, self).save(commit=False)
        message_instance.feed = self.feed
        message_instance.templar = self.templar

        message_instance.save()

class ReplyForm(forms.Form):
    text = forms.CharField(max_length=512,widget=forms.HiddenInput())
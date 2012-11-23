from django import forms
from models import Message

try:
    from notification import models as notification
except ImportError:
    notification = None

class RegisterForm(forms.Form):
    handel = forms.CharField(max_length=32,widget=forms.HiddenInput())
    public_key = forms.CharField(max_length=250,widget=forms.HiddenInput())
    pw_encrypted = forms.CharField(max_length=512,widget=forms.HiddenInput())
    pw_unencrypted = forms.CharField(max_length=128,widget=forms.HiddenInput())
    avatar_img = forms.CharField(max_length=16000,widget=forms.HiddenInput())

class MessageForm(forms.ModelForm):

    text = forms.CharField(label='',
        widget=forms.Textarea(attrs={
            'rows': '4',
            'cols':'30',
            'id':'new_message'
        }))

    class Meta:
        model = Message
        exclude = ('sender_type', 'sender_id', 'sent')

    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super(MessageForm, self).__init__(*args, **kwargs)

    def clean_text(self):
        return self.cleaned_data['text'].strip()

    def save(self):
        text = self.cleaned_data["text"]
        message_instance = super(MessageForm, self).save(commit=False)
        message_instance.sender = self.user
        message_instance.save()

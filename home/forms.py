from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, ExpertiseTags, Post, Comment, Votes

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    tag_OPTIONS = ExpertiseTags.objects.all().values('expertiseTagName')

    OPTIONS = []
    for index, tag in enumerate(tag_OPTIONS):
        OPTIONS.append((tag['expertiseTagName'], tag['expertiseTagName']))

    expertise_tags = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=OPTIONS)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['expertiseTags']


class PostUploadForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'tags', 'image']

class CommentUploadForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

class VoteUploadForm(forms.ModelForm):
    TRUE_FALSE_CHOICES = (
        (True, 'Phishing'),
        (False, 'Not Phishing')
    )

    positive = forms.ChoiceField(choices = TRUE_FALSE_CHOICES, label="Is this phishing?", 
                              initial='', widget=forms.Select(), required=True)

    class Meta:
        model = Votes
        fields = ["positive"]
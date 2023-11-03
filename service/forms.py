from django import forms
from django.contrib.auth.models import User

from .models import OrderComment, Profile


class OrderCommentForm(forms.ModelForm):
    class Meta:
        model = OrderComment
        fields = ["text"]


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email"]


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["picture"]

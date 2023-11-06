from django import forms
from django.contrib.auth.models import User

from .models import Order, OrderComment, Profile


class DateTimeInput(forms.DateInput):
    input_type = "datetime-local"


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["car", "deadline"]
        widgets = {"deadline": DateTimeInput()}


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

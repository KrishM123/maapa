from django import forms
from django.forms.widgets import MultiWidget
from WebApp.models import *



reason_for_use_choices = [
    ('school', 'School'),
    ('work', 'Work'),
    ('pp', 'Personal Project'),
    ('research', 'Research'),
    ('dev', 'Development'),
    ('other', 'Other')]
user_type_choices = [
    ('premium', 'Premium')]
class signUpForms(forms.Form):
    name = forms.CharField(required=True, widget=forms.TextInput({'placeholder': 'Enter you name'}))
    username = forms.CharField(required=True, widget=forms.TextInput({'placeholder': 'Set username'}))
    password = forms.CharField(required=True, widget=forms.TextInput({'placeholder': 'Set password'}))
    email = forms.EmailField(required=True, widget=forms.TextInput({'placeholder': 'Enter your email'}))
    reason_for_use = forms.ChoiceField(choices=reason_for_use_choices)
    user_type = forms.ChoiceField(choices=user_type_choices)



class loginForms(forms.Form):
    username = forms.CharField(required=True, widget=forms.TextInput({'placeholder': 'Username'}))
    password = forms.CharField(required=True, widget=forms.TextInput({'placeholder': 'Password'}))



class uploadResourceForms(forms.Form):
    document = forms.FileField(required=True)


class askQuestionForms(forms.Form):
    query = forms.CharField(required=True, widget=forms.Textarea(attrs={"rows":2, "cols":70}))
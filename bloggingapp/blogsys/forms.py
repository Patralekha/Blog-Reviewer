from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm,ReadOnlyPasswordHashField
from . models import User


class NewUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username','email',)

    def clean_email(self):
        email = self.cleaned_data['email']#get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("email is taken")
        return email

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data['password']#self.cleaned_data.get("password1")
        password2 = self.cleaned_data['password2']#self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

class NewBlogForm(forms.Form):
    blogtitle = forms.CharField(label='Blog Title',max_length=200)
    blogcontent = forms.CharField(widget=forms.Textarea,label='Blog Content',max_length=400)
    blogimg = forms.ImageField(label='Upload Image')

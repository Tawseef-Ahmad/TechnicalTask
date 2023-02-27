from django import forms
from app.models import MyUser

class AddUserForm(forms.ModelForm):
      class Meta:
            model = MyUser
            fields = '__all__'


class UserLoginForm(forms.Form):
    
    username = forms.CharField(widget=forms.TextInput(attrs={
		"class":"form-control form-control-user",
		"type":"text",
		"placeholder":"Username",
	}))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
			"class":"form-control form-control-user",
			"type":"password",
			"placeholder":"Enter password",
	}))


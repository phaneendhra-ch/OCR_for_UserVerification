from django import forms
from django.contrib.auth import get_user_model
from ocrapp.models import CustomRegister
from django.template.defaultfilters import mark_safe

User = get_user_model()
print(f'get user model is {User}')

class DateInput(forms.DateInput):
    input_type = 'date'

class LoginForm(forms.ModelForm):
    Aadhar_Num = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control','placeholder':'123456789111'}),label=mark_safe("<b>Enter Your 12-Digit Aadhar Number</b>"))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'password@125',}),label=mark_safe("<b>Enter Password</b>"))
    class Meta():
        model = User
        fields = ('Aadhar_Num','password')

class RegisterForm(forms.ModelForm):
    password_re = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'password@125',}),label=mark_safe("<b>Confirm Password</b>"))
    class Meta():
        model = CustomRegister
        fields = ('password_re','Name','DOB','GEN','AadharPic',)
        #DOB = forms.DateField(input_formats=['%D/%M/%Y'])
        widgets = {
            'Name' : forms.TextInput(attrs={'class':'form-control','placeholder':'John Kanenson'}),
            #'DOB' : forms.DateInput(attrs={'class':'form-control','placeholder':'YYYY-MM-DD'}),

            'DOB' : DateInput(attrs={'class':'btn btn-warning btn-lg'}),
            'GEN' : forms.Select(attrs={'class':'btn btn-info btn-sm dropdown-toggle'}),
            'AadharPic' : forms.FileInput(attrs={'id':'input-b2','class':'btn btn-dark btn-sm'}),
            #'AadharPic' : forms.FileInput(attrs={'class':'form-control input-sm'}) btn btn-dark
            }

        labels ={
            'Name':mark_safe('<b>Enter Your Full Name</b>'),
            'DOB':mark_safe('<b>Enter Your Date of Birth</b>'),
            'GEN':mark_safe('<b>Specify your Gender</b>'),
            'AadharPic': mark_safe('<b>Upload your Laminated Aadhar Card</b>'),
            }

class AadharUpdateForm(forms.ModelForm):
    class Meta():
        model=CustomRegister
        fields=('AadharPic',)
        widgets = {
            'AadharPic' : forms.FileInput(attrs={'id':'input-b2','class':'btn btn-dark btn-sm'}),
            }

class UpdateUserPassword(forms.ModelForm):
    Aadhar_Num = forms.IntegerField()
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'password@125',}),label=mark_safe("<b>Enter New Password</b>"))
    conf_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'password@125',}),label=mark_safe("<b>Confirm Password</b>"))
    class Meta():
        model = User
        fields = ('Aadhar_Num','password','conf_password')

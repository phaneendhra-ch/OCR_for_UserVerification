from rest_framework import serializers
from django.contrib.auth import get_user_model
from ocrapp.models import CustomRegister,Register


class TaskSerializers(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id','Aadhar_Num','is_verified','is_active','is_staff','is_superuser')


class LoginSerializers(serializers.ModelSerializer):

    password = serializers.CharField(
        style={'input_type': 'password',}
    )
    
    class Meta:
        model = Register
        fields = ('Aadhar_Num','password')

class RegisterSerializers(serializers.ModelSerializer):

    user = LoginSerializers(many=True, read_only=True)

    AadharPic = serializers.ImageField(max_length=None,
                                       use_url=True)
    class Meta:
        model = CustomRegister
        fields = ('Name','DOB','GEN','AadharPic','user')


class ChangePasswordSerializers(serializers.ModelSerializer):
    password = serializers.CharField( style={'input_type': 'password',},
                                      required=True,)
    password2 = serializers.CharField(style={'input_type': 'password',},
                                      required=True)
    old_password = serializers.CharField( style={'input_type': 'password',},
                                          required=True)

    class Meta:
        model = get_user_model()
        fields = ('old_password', 'password', 'password2')

class UpdateAadharSerializers(serializers.ModelSerializer):

    AadharPic = serializers.ImageField(max_length=None,
                                       use_url=True)
    class Meta:
        model = CustomRegister
        fields = ('AadharPic',)

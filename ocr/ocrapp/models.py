from django.db import models
from django.contrib.auth.models import AbstractBaseUser,AbstractUser,BaseUserManager,PermissionsMixin
from django.core.validators import MaxValueValidator, MinValueValidator,RegexValidator
from django import forms
from django.contrib.auth import get_user_model

# Create your validators here.

Name_Validator = RegexValidator(r'^[a-zA-Z\s]*$',
                                message = "This field accepts only alphabetical characters.")

Image_Validator = RegexValidator(r".jpg$|.jpeg$|.png$",
                                message = "Image should contain .jpeg, .jpg, .png formats only.")

# Create your models here.
class CustomManager(BaseUserManager):
    def create_user(self,Aadhar_Num,password=None,**other_fields):

        if not Aadhar_Num:
            raise ValueError('Provide a valid aadhar card number')

        user = self.model(Aadhar_Num = Aadhar_Num,
                        **other_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,Aadhar_Num,password=None,**other_fields):
        other_fields.setdefault('is_staff',True)
        other_fields.setdefault('is_superuser',True)
        other_fields.setdefault('is_active',True)
        other_fields.setdefault('is_verified',True)
        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be true is_staff')

        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be true is_superuser')

        return self.create_user(Aadhar_Num, password, **other_fields)

class Register(AbstractBaseUser,PermissionsMixin):

    Aadhar_Num = models.IntegerField(unique=True,
                                    null=False,
                                    blank=False,
                                    verbose_name="Enter Your Aadhar Number",
                                    validators=[MaxValueValidator(999999999999),
                                    MinValueValidator(100000000000)])

    is_active = models.BooleanField(default=True,
                                    blank=True)
    is_staff = models.BooleanField(default=False,
                                    blank=True)
    is_superuser = models.BooleanField(default=False,
                                       blank = True)
    date_joined = models.DateTimeField(verbose_name='date joined',
                                        auto_now_add = True,
                                        blank = True)

    last_login = models.DateTimeField(verbose_name='last login',
                                     auto_now=True,
                                     blank = True)

    is_verified = models.BooleanField(default=False,
                                      blank=True)

    objects = CustomManager()

    USERNAME_FIELD = 'Aadhar_Num'
    REQUIRED_FIELDS = []

    def __str__(self):
        return str(self.Aadhar_Num)

class CustomRegister(models.Model):

    GENDER_CHOICES  = (
    ('male','Male'),
    ('female','Female'),
    ('others','Others'),
    )
    user = models.OneToOneField(Register,on_delete=models.CASCADE,)

    Name = models.CharField(null=False,
                            blank=False,
                            max_length=50,
                            verbose_name="Enter Your Full Name",
                            validators=[Name_Validator])

    DOB = models.DateField(null=False,
                          )

    GEN = models.CharField(max_length=6,
                           verbose_name="Specify your Gender",
                           choices=GENDER_CHOICES)
    AadharPic = models.ImageField(blank=False,
                                  upload_to='AadharPic',
                                  verbose_name='Upload your Laminated Aadhar Card',
                                  validators = [Image_Validator],
                                  help_text="<br><div style='color:red'><b>*  Image should contain .jpeg, .jpg, .png formats only.  *</b></div>",)
    def __str__(self):
        return str(self.user.Aadhar_Num)

    def save(self, *args, **kwargs):
        self.Name = self.Name.lower()
        return super(CustomRegister, self).save(*args, **kwargs)

from django.shortcuts import render,redirect
from ocrapp.forms import LoginForm, RegisterForm, AadharUpdateForm, UpdateUserPassword
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from django.http import HttpResponseRedirect,HttpResponse,JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.urls import reverse
from ocrapp.models import Register,CustomRegister
from ocrfiles import main
import time
import json

from rest_framework.decorators import api_view,permission_classes,parser_classes, authentication_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.parsers import FormParser, MultiPartParser, FileUploadParser
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from ocrapp.serializers import TaskSerializers, LoginSerializers, RegisterSerializers, ChangePasswordSerializers, UpdateAadharSerializers

#getalldata
@api_view(['GET'])
def getallusers(request):
    users = Register.objects.all()
    serializer = TaskSerializers(users,many=True)
    return Response(serializer.data)

#get a user through id as a primary key.
@api_view(['GET'])
def getspecificuser(request, pk):
    try:
        users = Register.objects.get(id=pk)
        serializer = TaskSerializers(users,many=False)
        return Response(serializer.data)
    except:
        return Response(f'User is not registered with Id:{pk}')

@api_view(['GET','POST'])
@permission_classes([AllowAny])
def createtoken(request):
    if request.method == "POST":
        Aadhar_Num = request.POST.get('Aadhar_Num')
        password = request.POST.get('password')
        user  = authenticate(Aadhar_Num = Aadhar_Num,
                                 password = password)
        if user:
            return Response(f'{user} is a valid user')
        else:
            return Response('No user is associated with these credentials')
    else:
        return Response('Get your token here')

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def getalluserstoken(request):
    users = Register.objects.filter(id=request.user.id)
    serializer = TaskSerializers(users,many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def updatepasswordapi(request):
    if request.method == "POST":
        Change_Password_Serializers = ChangePasswordSerializers(data = request.POST)
        if Change_Password_Serializers.is_valid():
            current_password= request.user.password #user's current password
            #print(Change_Password_Serializers.data)
            matchcheck= check_password(Change_Password_Serializers.data['old_password'],current_password)
            if matchcheck:
                if Change_Password_Serializers.data['password'] == Change_Password_Serializers.data['password2']:
                    user = Register.objects.get(Aadhar_Num=request.user.Aadhar_Num)
                    user.set_password(Change_Password_Serializers.data['password'])
                    user.save()
                    return Response('Password updated successfully!!')
                else:
                    return Response('Passwords didnt match')
            else:
                return Response('Incorrect Existing Password')
        else:
            return Response('Please fill all the required fields')
    else:
        return Response('Update your password here !! ')

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def updateaadharapi(request):

    if request.method == "POST":

        #delete old photo, if existing.
        form_aux = UpdateAadharSerializers(data=request.data)
        if form_aux.is_valid() and 'AadharPic' in request.data:
            request.user.customregister.AadharPic.delete()

        #add new photo
        Update_Aadhar_Serializers= UpdateAadharSerializers(data = request.data,instance = request.user.customregister)
        if Update_Aadhar_Serializers.is_valid():
            Update_Aadhar_Serializers.save()

        return Response('Aadhar image successfully updated')

    else:
        return Response('You can update your aadhar image here. * Only .jpeg, .jpg and .png files are accepted * ')

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def checkstatus(request):
    if request.method == "POST":
        checkuser = request.user.is_verified
        if checkuser is True:
            return Response(f" Verified : {checkuser} ")
        else:
            your_details = list(Register.objects.filter(id=request.user.id))
            your_details_onetoone = list(CustomRegister.objects.all().filter(user_id = your_details[0].id))
            your_details_onetoone_dict = CustomRegister.objects.filter(user_id = your_details[0].id).values('Name','DOB','GEN')
            duplicate = dict(your_details_onetoone_dict[0])

            your_details_onetoone_dict = your_details_onetoone_dict[0]
            dob_key = "Date of Birth"
            gender_key = "Gender"

            your_details_onetoone_dict[dob_key] = your_details_onetoone_dict.pop('DOB')
            your_details_onetoone_dict[dob_key] = your_details_onetoone_dict.get(dob_key).strftime('%d/%m/%Y')
            your_details_onetoone_dict[gender_key] = your_details_onetoone_dict.pop('GEN')
            your_details_onetoone_dict['Name'] = your_details_onetoone_dict.get('Name').title()
            try :
                getinfoocr = main.insertimg("."+request.user.customregister.AadharPic.url)
                if ((getinfoocr['aadharnum'] == request.user.Aadhar_Num)
                    and (getinfoocr['name'] == duplicate['Name'])
                    and (getinfoocr['dob'] == your_details_onetoone_dict['Date of Birth'])
                    and (getinfoocr['gender'] == your_details_onetoone_dict['Gender'])):
                    print('yes')
                    sample_user = Register.objects.get(id=request.user.id)
                    print('Before Validating ....')
                    print(sample_user.is_verified)
                    print('After Validating ....')
                    sample_user.is_verified = True
                    sample_user.save()
                    print(sample_user.is_verified)
                    return Response("Successully Verified User.")
                else:
                    #return Response("Inappropiate image or details didnt match")
                    your_details_onetoone_dict['AadharNumber'] = request.user.Aadhar_Num
                    context = {'OCR Extracted Info':getinfoocr,
                               'User Info':your_details_onetoone_dict,
                               'Verdict' : "Details Didnt Match",}
                    return Response(context)
            except:
                #return Response('Servers Busy, Try Again later..')
                return Response('Sorry we couldnt fetch any details. Please upload a valid Aadhar Pic!!')
    else:
        return Response("You can check your status here. !")

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser,FileUploadParser])
def user_registration_serializer(request):
    if request.method == "POST":
        Login_Form_Serializers= LoginSerializers(data = request.POST)
        Register_Form_Serializers= RegisterSerializers(data = request.data)
        if Login_Form_Serializers.is_valid() and Register_Form_Serializers.is_valid():
            user = Login_Form_Serializers.save()
            user.set_password(user.password)
            user.save()
            #print(f'saved through forms : {user}')
            '''
            createduser = Register.objects.create(Aadhar_Num=Login_Form_Serializers.data['Aadhar_Num'],
                                                  password=Login_Form_Serializers.data['password'])
            '''
            CustomRegister.objects.create(user = user,
                                          Name = Register_Form_Serializers.data['Name'],
                                          DOB = Register_Form_Serializers.data['DOB'],
                                          GEN = Register_Form_Serializers.data['GEN'],
                                          AadharPic = request.data['AadharPic'])

            return Response("User Created Successully")
        else:
            return Response(Login_Form_Serializers.errors)
    else:
        return Response("Register Here")


# Create your views here.

def index(request):
    return render(request,'ocrapp/base.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('tempindex')
    #return HttpResponseRedirect(reverse('tempindex'))

def register(request):
    user_registered = False
    imagereq = "* Only .jpeg, .jpg and .png files are accepted *"
    if request.method == "POST":
        Register_Form = RegisterForm(request.POST,request.FILES)
        Login_Form = LoginForm(request.POST)
        print(Login_Form)
        print(Register_Form)
        p2 = Register_Form['password_re'].value()
        p1 = Login_Form['password'].value()
        if p1==p2 :
            if Login_Form.is_valid() and Register_Form.is_valid():
                user = Login_Form.save()
                user.set_password(user.password)
                user.save()

                register_user = Register_Form.save(commit = False)
                register_user.user = user

                if 'AadharPic' in request.FILES:
                    register_user.AadharPic  = request.FILES['AadharPic']

                register_user.save()
                user_registered = True
                #time.sleep(3.5)
                #return redirect('templogin')
                #user_registered = True
            else:
                print("form failed")
                Register_Form = RegisterForm()
                Login_Form = LoginForm()
                print(Register_Form.errors)
                #return HttpResponse('NOT A VALID FORM.')
        else:
            messages.info(request, 'Passwords doesnt match !!')
            return render(request,'ocrapp/register.html',{'showmessage':True})
    else:
        Register_Form = RegisterForm()
    #return render(request,'ocrapp/register.html',{'login_form':LoginForm,'Register_Form':Register_Form,'user_registered':user_registered,'imagereq':imagereq})
    return render(request,'ocrapp/register.html',{'login_form':LoginForm,'Register_Form':Register_Form,'user_registered':user_registered,'showmessage':False})

#@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def user_login(request):

    if request.method == "POST":
        Aadhar_Num = request.POST.get('Aadhar_Num')
        password = request.POST.get('password')
        print(Aadhar_Num,password)
        user = authenticate(Aadhar_Num = Aadhar_Num,password = password)
        print(user)
        if user:
            if user.is_active:
                login(request,user)
                #return redirect('tempindex')
                return redirect('verifypage')
                #return HttpResponseRedirect(reverse('tempindex'))
            else:
                return HttpResponse('Your Account was temporarily Down!!')
        else:
            #UserDoesntExist = True
            return render(request,'ocrapp/login.html',{'login_form':LoginForm,'UserDoesntExist':True})
    else:
        return render(request,'ocrapp/login.html',{'login_form':LoginForm})

@login_required
def updatepassword(request):
    if request.method == "POST":
        oldpass = request.POST.get('oldpassword')
        current_password= request.user.password #user's current password
        matchcheck= check_password(oldpass,current_password)
        if matchcheck:
            p1 = request.POST.get('password')
            p2 = request.POST.get('Confirm_password')
            if p1 == p2:
                user = Register.objects.get(Aadhar_Num=request.user.Aadhar_Num)
                user.set_password(p1)
                user.save()
                login(request,user)
                messages.success(request, 'Your password was successfully updated!')
                #return render(request,'ocrapp/changepassword.html')
                return redirect('verifypage')
            else:
                messages.info(request, 'Your passwords didnt match!')
                return render(request,'ocrapp/changepassword.html')
                #return HttpResponse('Passwords Didnt Match')
        else:
            messages.info(request, 'Incorrect Existing Password')
            return render(request,'ocrapp/changepassword.html')
    else:
        return render(request,'ocrapp/changepassword.html')

@login_required
def getusers(request):
    sample_user = Register.objects.get(id=request.user.id)
    print(sample_user)
    print(sample_user.is_verified)
    context_ = CustomRegister.objects.values()
    return HttpResponse(context_)

@login_required
def uploadAadhar(request):
    if request.method == "POST":

        #deletes old image in case of new image upload
        form_aux = AadharUpdateForm(data=request.POST, files=request.FILES)
        if form_aux.is_valid() and 'AadharPic' in request.FILES:
            request.user.customregister.AadharPic.delete()

        AadharUpdate_Form = AadharUpdateForm(request.POST,request.FILES,instance=request.user.customregister)
        if AadharUpdate_Form.is_valid():
            AadharUpdate_Form.save()
            return redirect('verifypage')
        else:
            AadharUpdate_Form = AadharUpdateForm(instance=request.user.customregister)
    else:
        AadharUpdate_Form = AadharUpdateForm()
    return render(request,'ocrapp/UpdateAadhar.html',{'AadharUpdate_Form':AadharUpdate_Form})

@login_required
def comparedetails(request):
    '''
    current_user = CustomRegister.objects.all().filter(user_id = request.user.id).values()
    return HttpResponse(current_user)
    '''
    checkuser = request.user.is_verified
    if checkuser is True:
        return render(request,'ocrapp/postlogin.html',)
    else:
        pass
    try :
        print(request.user.customregister.AadharPic.url)
        your_details = list(Register.objects.filter(id=request.user.id))
        your_details_onetoone = list(CustomRegister.objects.all().filter(user_id = your_details[0].id))
        #your_details_onetoone_dict = CustomRegister.objects.all().filter(user_id = your_details[0].id).values('Name','DOB','GEN','AadharPic')
        your_details_onetoone_dict = CustomRegister.objects.filter(user_id = your_details[0].id).values('Name','DOB','GEN')
        #print(f'from queryset : {your_details[0].id} {your_details_onetoone[0]}')
        duplicate = dict(your_details_onetoone_dict[0])
        print(duplicate)

        your_details_onetoone_dict = your_details_onetoone_dict[0]
        dob_key = "Date of Birth"
        gender_key = "Gender"

        your_details_onetoone_dict[dob_key] = your_details_onetoone_dict.pop('DOB')
        your_details_onetoone_dict[dob_key] = your_details_onetoone_dict.get(dob_key).strftime('%d/%m/%Y')
        your_details_onetoone_dict[gender_key] = your_details_onetoone_dict.pop('GEN')
        your_details_onetoone_dict['Name'] = your_details_onetoone_dict.get('Name').title()
        try :
            getinfoocr = main.insertimg("."+request.user.customregister.AadharPic.url)
            if ((getinfoocr['aadharnum'] == request.user.Aadhar_Num)
                and (getinfoocr['name'] == duplicate['Name'])
                and (getinfoocr['dob'] == your_details_onetoone_dict['Date of Birth'])
                and (getinfoocr['gender'] == your_details_onetoone_dict['Gender'])):
                print('yes')
                sample_user = Register.objects.get(id=request.user.id)
                print('Before Validating ....')
                print(sample_user.is_verified)
                print('After Validating ....')
                sample_user.is_verified = True
                sample_user.save()
                print(sample_user.is_verified)
                time.sleep(2.5)
                return render(request,'ocrapp/postlogin.html',)
            else:
                print("Inappropiate image or details didnt match")
                show_details =True
                return render(request,'ocrapp/postlogin.html',{'show_details':show_details,'getinfoocrdetails':getinfoocr,'your_details_onetoone':your_details_onetoone_dict})
        except:
            print('ocr didnt find anything')
            return render(request,'ocrapp/postlogin.html',{'invalid':'Sorry we couldnt fetch any details. Please upload a valid Aadhar Pic!!'})
        #getinfoocr = main.insertimg("."+request.user.customregister.AadharPic.url)
        print(your_details_onetoone_dict)
        print(getinfoocr)
        return render(request,'ocrapp/postlogin.html',{'invalid':'Sorry we couldnt fetch any details.Try uploading your aadhar pic once more!!'})
    except:
        return render(request,'ocrapp/postlogin.html',)

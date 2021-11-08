"""ocr URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls import url,include,static
from django.views.decorators.csrf import csrf_exempt
from ocrapp.views import *
from rest_framework.authtoken import views

urlpatterns = [
    ##Forms below.
    url(r'^adminadda/', admin.site.urls),                                                      #URL for admin site.
    url(r'^$',index,name='tempindex'),                                                         #index URL.
    url(r'^login/$',user_login,name="templogin"),                                              #URL for login page.
    url(r'^register/$',register,name="tempregister"),                                          #URL for Registration page.
    url(r'^logout/$',user_logout,name="templogout"),                                           #URL for logout --> Login Required.
    url(r'^getusers/$',getusers,name="get_users"),                                             #sample HttpResponse page.
    url(r'^statuspage/$',comparedetails,name="verifypage"),                                    #URL to Verify the identity of user --> Login Required.
    url(r'^updateaadhar/$',uploadAadhar,name="updateaadharpic"),                               #URL to update User Aadhar Image --> Login Required.
    url(r'^updatepassword/$',updatepassword,name="updatepassword"),                            #URL to update/change User Password --> Login Required.

    ##Api below.
    url(r'^api/getallusers/$',getallusers,name='getallusers'),                                  #get all users in database
    url(r'^api/getspecificuser/(?P<pk>\d+)/$',getspecificuser,name='getspecificuser'),          #can retreive specific user details through ID as PK
    url(r'^api/gettoken/$',createtoken,name="manualtoken"),
    url(r'^api/registration/$',user_registration_serializer,name='userregistrationserializer'), #A new user can be registered here. --> Authentication Required
    url(r'^api-token-auth/$', views.obtain_auth_token,name="gettoken"),                         #Existing User can get a token here, to access the API's --> Authentication Required
    url(r'^api/getalluserstoken/$',getalluserstoken,name='getalluserstoken'),                   #can retreive specific user details here --> Authentication Required
    url(r'^api/updatepasswordapi/$',updatepasswordapi,name="updatepasswordapi"),                #A user can change his/her password here --> Authentication Required
    url(r'^api/updateaadharapi/$',updateaadharapi,name="updateaadharapi"),                      #A user can update his/her Aadhar Image here --> Authentication Required
    url(r'^api/checkstatusapi/$',checkstatus,name="checkstatusapi"),                            #A user can check his identity here --> Authentication Required
]
if settings.DEBUG:
    urlpatterns += static.static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

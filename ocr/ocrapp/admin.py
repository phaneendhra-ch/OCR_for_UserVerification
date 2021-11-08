from django.contrib import admin
from ocrapp.models import Register,CustomRegister
from django.contrib.auth.admin import UserAdmin
# Register your models here.

#admin.site.register(Register)
#admin.site.register(CustomRegister)

class UserAdminConfig(UserAdmin):
    model = Register
    search_fields = ('Aadhar_Num','id',)
    list_filter = ('is_verified','is_staff','is_active','date_joined',)
    ordering = ('id',)
    list_display = ('Aadhar_Num','id','is_active','last_login','is_verified','is_staff',)

    fieldsets = (
    ('User Info',{'fields':('Aadhar_Num','password',)}),
    ('Permissions',{'fields':('is_active','is_staff','is_verified')})
    )

    class Media:
        js = ('js/admin/placeholderMainModel.js',)

admin.site.register(Register, UserAdminConfig)

class UserAdminConfigModel(admin.ModelAdmin):
    model = CustomRegister
    search_fields = ('Name','user__id',)
    list_filter = ('GEN',)
    ordering = ('user_id',)
    list_display = ('user','user_id','Name','DOB','GEN','AadharPic',)

    class Media:
        js = ('js/admin/placeholderOneToOne.js',)

admin.site.register(CustomRegister, UserAdminConfigModel)

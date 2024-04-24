from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.admin import UserAdmin
from .forms  import CustomUserChangeForm,CustomUserCrerationForm
from .models import CustomUser



# class UserAdmin(BaseUserAdmin):
#     add_form = UserCreationForm
#     form = UserChangeForm
#     model = CustomUser
#     list_display = ['username', 'email', 'description']
#     fieldsets = BaseUserAdmin.fieldsets + (
#         (None, {'fields': ('description',)}),
#     )
#     add_fieldsets = BaseUserAdmin.add_fieldsets + (
#         (None, {'fields': ('description',)}),
#     )

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'fname', 'lname', 'username', 'password', 'phone', 'address', 'createdAt', 'updatedAt', 'AccessLevel')  # اضافه کردن AccessLevel

admin.site.register(CustomUser, UserAdmin)

from django.contrib import admin
from .models import UserAccount, UserInformation

# Register your models here.
admin.site.register(UserAccount)
admin.site.register(UserInformation)

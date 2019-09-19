from django.contrib import admin
from auto.models import User
# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('u_name', 'u_last_time')  # list
    fields = ('u_name','u_last_time')
admin.site.register(User,UserAdmin)

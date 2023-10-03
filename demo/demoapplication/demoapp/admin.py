from django.contrib import admin
from .models import Registration
# Register your models here.
class RegistrationAdmin(admin.ModelAdmin):
    list_display=('fname','lname','email','passwd','role','jno', 'sal', 'cdate', 'dob','img')

admin.site.register(Registration,RegistrationAdmin)
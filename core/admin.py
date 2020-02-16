from django.contrib import admin

from .models import Emplyee,Event,UserProfile
class EventAdmin(admin.ModelAdmin):
    list_display = ['id','emplyee','user','time','time_added','enter']

admin.site.register(Emplyee)
admin.site.register(Event,EventAdmin)
admin.site.register(UserProfile)
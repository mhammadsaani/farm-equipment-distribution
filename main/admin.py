from django.contrib import admin
from .models import Profile, Settings, Notification, SearchHistory

# Register your models here.
admin.site.register(Profile)
admin.site.register(Settings)
admin.site.register(Notification)
admin.site.register(SearchHistory)

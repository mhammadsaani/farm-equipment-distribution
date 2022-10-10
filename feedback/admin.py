from django.contrib import admin
from .models import Form, QuestionField, Response

# Register your models here.
admin.site.register(Form)
admin.site.register(QuestionField)
admin.site.register(Response)

from django.contrib import admin
from .models import Items, Heroes, Answer, UserData


admin.site.register([Items, Heroes, Answer, UserData])

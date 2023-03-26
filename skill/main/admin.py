from django.contrib import admin
from .models import Heroes, Answer


admin.site.register([Heroes, Answer])

from django.contrib import admin
from .models import tournament
from .matches import matche

admin.site.register(tournament)
admin.site.register(matche)

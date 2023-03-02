from django.contrib import admin
from .models import Player,Category,Result,Question

# Register your models here.

admin.site.register(Player)
admin.site.register(Category)
admin.site.register(Result)
admin.site.register(Question)
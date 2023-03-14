from django.contrib import admin
from .models import Player,CustomQuiz,Result,Question

# Register your models here.

admin.site.register(Player)
admin.site.register(CustomQuiz)
admin.site.register(Result)
admin.site.register(Question)
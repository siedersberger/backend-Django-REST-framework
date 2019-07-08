from django.contrib import admin
from .models import Roteiro, Passeio, Localizacao

# Register your models here.
admin.site.register(Roteiro)
admin.site.register(Passeio)
admin.site.register(Localizacao)
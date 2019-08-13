from django.contrib import admin
from .models import Passeio, Localizacao, Disponibilidade

admin.site.register(Localizacao)
admin.site.register(Passeio)
admin.site.register(Disponibilidade)
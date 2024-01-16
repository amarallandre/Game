
from django.contrib import admin
from django.urls import path, include

from Game.views import Char_Creator

urlpatterns = [
    path('', Char_Creator, name='Char_Creator'),
    path('admin/', admin.site.urls),
    path('Game/', include('Game.urls')),
]

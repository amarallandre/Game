from django.urls import path

from .views import Char_Creator, get_all_chars, delete_char, select_char, game_page

urlpatterns = [
    path('Main/', Char_Creator, name='Char_Creator'),
    path('get_all_chars/', get_all_chars, name='get_all_chars'),
    path('delete_char/', delete_char, name='delete_char'),
    path('select_char/', select_char, name='select_char'),
    path('Game.html', game_page, name='Game.html'),
]

from django.urls import path

from .views import index, texte, add, add_mvt, add_author


app_name = 'Presentation'
urlpatterns = [
    path('', index, name='index'),
    path('ajouter/', add, name='add'),
    path('ajouter-auteur/', add_author, name='add_author'),
    path('add_mvt/', add_mvt, name='add_mvt'),
    path('<str:key>/', texte, name='texte'),
]

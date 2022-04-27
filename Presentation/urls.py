
from django.urls import path

from .views import index, texte, add, add_author


app_name = 'Presentation'
urlpatterns = [
    path('', index, name='index'),
    path('ajouter/', add, name='add'),
    path('ajouter-auteur/', add_author, name='add_author'),
    path('<str:key>/', texte, name='texte'),
]

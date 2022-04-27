
from django.contrib import admin
from django.urls import path, include
from .views import main


app_name = 'OralBAC'
urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', main, name='main'),
    path('texte/', include('Presentation.urls')),
]

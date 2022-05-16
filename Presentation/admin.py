
from django.contrib import admin
from django.contrib.auth.models import User, Group

from .models import Texte, Auteur, Mouvement, Ligne


class LigneInline(admin.TabularInline):
    model = Ligne
    extra = 6

class TextAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Introduction', {'fields':('title', 'auteur', 'presentation', 'problematique')}),
        ('Conclusion', {'fields':('texte_conclusion', 'ouverture')})
    ]

class MouvementAdmin(admin.ModelAdmin):
    inlines = (LigneInline, )

# admin.site.unregister(User)
# admin.site.unregister(Group)

admin.site.register(Auteur)
admin.site.register(Texte, TextAdmin)
admin.site.register(Mouvement, MouvementAdmin)
admin.site.register(Ligne)
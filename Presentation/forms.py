
from django.forms import ModelForm, ModelChoiceField, inlineformset_factory

from .models import Texte, Auteur, Mouvement, Ligne
from .utils import RelatedFieldWidgetCanAdd

class AuteurForm(ModelForm):
    class Meta:
        model = Auteur
        fields = '__all__'


class MouvementForm(ModelForm):
    class Meta:
        model = Mouvement
        exclude = ('texte', )


class TexteForm(ModelForm):
    
    auteur = ModelChoiceField(
       required=False,
       queryset=Auteur.objects.all(),
       widget=RelatedFieldWidgetCanAdd(Auteur, related_url="Presentation:add_author")
                                )

    class Meta:
        model = Texte
        fields = '__all__'

MouvementInlineFormSet = inlineformset_factory(Texte, Mouvement, exclude=('texte',), extra=2)

LigneInlineFormSet = inlineformset_factory(Mouvement, Ligne, exclude=('mouvement',), extra=1)






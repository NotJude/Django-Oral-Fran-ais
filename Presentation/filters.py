
import django_filters

from .models import Texte


class TexteFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    class Meta:
        model = Texte
        fields = ('title', 'auteur')
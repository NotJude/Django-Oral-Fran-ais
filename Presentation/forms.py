# S/O to philgyford : 
# https://github.com/philgyford/django-nested-inline-formsets-example/tree/main/publishing/books


from django.forms import ModelForm, ModelChoiceField, inlineformset_factory, BaseInlineFormSet
from django.utils.translation import gettext_lazy as _

from .models import Texte, Auteur, Mouvement, Ligne
from .utils import RelatedFieldWidgetCanAdd, is_empty_form, is_form_persisted


class AuteurForm(ModelForm):
    class Meta:
        model = Auteur
        fields = '__all__'


"""class TexteForm(ModelForm):
    
    auteur = ModelChoiceField(
       required=False,
       queryset=Auteur.objects.all(),
       widget=RelatedFieldWidgetCanAdd(Auteur, related_url="Presentation:add_author")
                                )

    class Meta:
        model = Texte
        fields = '__all__'"""



# The formset for editing the Ligne that belong to a Mouvement.
LigneFormset = inlineformset_factory(
    Ligne, Mouvement, exclude=('child', ), extra=4
)


class BaseMouvementFormset(BaseInlineFormSet):
    """
    The base formset for editing Mouvements belonging to a Texte, and the
    Ligne belonging to those Mouvements.
    """

    def add_fields(self, form, index):
        super().add_fields(form, index)

        # Save the formset for a Child's Images in the nested property.
        form.nested = LigneFormset(
            instance=form.instance,
            data=form.data if form.is_bound else None,
            files=form.files if form.is_bound else None,
            prefix="Address-%s-%s"
            % (form.prefix, LigneFormset.get_default_prefix()),
        )

    def is_valid(self):
        """
        Also validate the nested formsets.
        """
        result = super().is_valid()

        if self.is_bound:
            for form in self.forms:
                if hasattr(form, "nested"):
                    result = result and form.nested.is_valid()

        return result

    def clean(self):
        """
        If a parent form has no data, but its nested forms do, we should
        return an error, because we can't save the parent.
        For example, if the Mouvement form is empty, but there are Lignes.
        """
        super().clean()

        for form in self.forms:
            if not hasattr(form, "nested") or self._should_delete_form(form):
                continue

            if self._is_adding_nested_inlines_to_empty_form(form):
                form.add_error(
                    field=None,
                    error=_(
                        "Vous êtes en train d'essayer d'ajouter une Ligne à "
                        "un Mouvement qui n'existe pas encore. Veuillez "
                        "ajouter des informations à propos de ce(s) "
                        "Mouvement(s) et remplissez de nouveau les Lignes"
                    ),
                )

    def save(self, commit=True):
        """
        Also save the nested formsets.
        """
        result = super().save(commit=commit)

        for form in self.forms:
            if hasattr(form, "nested"):
                if not self._should_delete_form(form):
                    form.nested.save(commit=commit)

        return result

    def _is_adding_nested_inlines_to_empty_form(self, form):
        """
        Are we trying to add data in nested inlines to a form that has no data?
        e.g. Adding Lignes to a new Mouvement whose data we haven't entered?
        """
        if not hasattr(form, "nested"):
            # A basic form; it has no nested forms to check.
            return False

        if is_form_persisted(form):
            # We're editing (not adding) an existing model.
            return False

        if not is_empty_form(form):
            # The form has errors, or it contains valid data.
            return False

        # All the inline forms that aren't being deleted:
        non_deleted_forms = set(form.nested.forms).difference(
            set(form.nested.deleted_forms)
        )

        # At this point we know that the "form" is empty.
        # In all the inline forms that aren't being deleted, are there any that
        # contain data? Return True if so.
        return any(not is_empty_form(nested_form) for nested_form in non_deleted_forms)


# This is the formset for the Mouvements belonging to a Texte and the
# Lignes belonging to those Mouvements.
#
# You'd use this by passing in a Texte:
#     TexteMouvementFormset(**form_kwargs, instance=self.object)
ChildrenFormset = inlineformset_factory(
    Texte,
    Mouvement,
    formset=BaseMouvementFormset,
    # We need to specify at least one Mouvement field:
    exclude=('parent',),
    extra=3,
    # If you don't want to be able to delete Textes:
    # can_delete=False
)



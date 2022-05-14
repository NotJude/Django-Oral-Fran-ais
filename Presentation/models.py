
from django.db import models
# from django.utils.crypto import get_random_string
import uuid

class Auteur(models.Model):
    name = models.CharField(max_length=50)
    birth_date = models.DateField("Birth Year")
    death_date = models.DateField("Year of Death")
    description = models.TextField()

    def __str__(self):
        return self.name


class Texte(models.Model):
    url = models.UUIDField(
            default=uuid.uuid4,
            unique=True,
            editable=False
        )
    title = models.CharField(max_length=50, blank=True)
    auteur = models.ForeignKey(Auteur, on_delete=models.CASCADE, null=True)
    presentation = models.TextField()
    problematique = models.CharField(max_length=500)
    texte_conclusion = models.TextField()
    ouverture = models.TextField()

    def __str__(self):
        return self.title


class Mouvement(models.Model):
    texte = models.ForeignKey(Texte, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=True)
    range = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return str(self.texte) + ' ' + str(self.pk)


class Ligne(models.Model):
    mouvement = models.ForeignKey(Mouvement, on_delete=models.CASCADE, null=True)
    citation = models.CharField(max_length=250, blank=True, null=True)
    outil = models.CharField(max_length=250, blank=True, null=True)
    analyse = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return str(self.mouvement) + str(self.pk)




from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


# listings/models.py

class Band(models.Model):

    class Genre(models.TextChoices):
        HIP_HOP = 'HH'
        SYNTH_POP = 'SP'
        ALTERNATIVE_ROCK = 'AR'

    name = models.fields.CharField(max_length=100)
    genre = models.fields.CharField(max_length=50)
    biography = models.fields.CharField(max_length=1000, default="Biographie par défaut")
    year_formed = models.fields.IntegerField(
    validators=[MinValueValidator(1900), MaxValueValidator(2024)]
    )
    active = models.fields.BooleanField(default=True)
    official_homepage = models.fields.URLField(null=True, blank=True)
    genre = models.fields.CharField(choices=Genre.choices, max_length=5)
    def __str__(self):
        return f'{self.name}'

class Listing(models.Model):
    class Type(models.TextChoices):
        RECORDS = 'REC', 'Disques'
        CLOTHING = 'CLO', 'Vêtements'
        POSTERS = 'POS', 'Affiches'
        MISCELLANEOUS = 'MIS', 'Divers'

    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    sold = models.BooleanField(default=True)
    year = models.IntegerField(validators=[MinValueValidator(1900), MaxValueValidator(2024)])
    types = models.CharField(choices=Type.choices, max_length=30)
    band = models.ForeignKey(Band, null=True, on_delete=models.SET_NULL)
    like_new = models.fields.BooleanField(default=False)

    def __str__(self):
        return self.title
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator


from .choices import GENDERS, COUNTRIES

## USERS
# so we can also login with username -> we modify the CustomUserManager to check either un or email
from django.contrib.auth.models import UserManager
from django.db.models import Q
class CustomUserManager(UserManager):
    def get_by_natural_key(self, username):
        return self.get(
            Q(**{self.model.USERNAME_FIELD: username}) | Q(**{self.model.EMAIL_FIELD: username})
        )


class CustomUser(AbstractUser):
    objects = CustomUserManager()
    email = models.EmailField(unique=True, error_messages={'unique': 'A user with that email already exists'})
    first_name = models.CharField(max_length=50, blank=False, null=False)
    last_name = models.CharField(max_length=50, blank=False, null=False)
    date_of_birth = models.DateField()
    country = models.CharField(max_length=2, choices=COUNTRIES)
    gender = models.CharField(max_length=1, choices=GENDERS)

    #relationships - django will create the reverse relationships (no need to set mods on festival)
    festivals = models.ManyToManyField('Festival', related_name='mods')


## FESTIVALS
class Festival(models.Model):
    # name should be unique
    name = models.CharField(max_length=50)
    info = models.TextField(blank=True, default='No info provided')
    website = models.URLField(blank=True, default='No website provided')
    lat = models.FloatField(blank=True, null=True)
    lon = models.FloatField(blank=True, null=True)

    class Meta:
        ordering = ['name']


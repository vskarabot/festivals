from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator


from .choices import GENDERS, POST_LABELS, COUNTRIES

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
    # username is automatically implemented
    email = models.EmailField(unique=True, error_messages={'unique': 'A user with that email already exists'})
    first_name = models.CharField(max_length=50, blank=False, null=False)
    last_name = models.CharField(max_length=50, blank=False, null=False)
    date_of_birth = models.DateField()
    country = models.CharField(max_length=2, choices=COUNTRIES)
    gender = models.CharField(max_length=1, choices=GENDERS)

    #relationships - django will create the reverse relationships (no need to set mods on festival)
    festivals = models.ManyToManyField('Festival', related_name='mods')
    favourite_festivals = models.ManyToManyField('Festival', related_name='favourite_by')


## FESTIVALS
class Festival(models.Model):
    # name should be unique
    name = models.CharField(max_length=50)
    info = models.TextField(blank=True, default='No info provided')
    website = models.URLField(blank=True, default='No website provided')
    lat = models.FloatField(blank=True, null=True)
    lon = models.FloatField(blank=True, null=True)
    
    # null=True so we dont break model - only for testing!!!!!!!!!!
    # TODO : delete those values when creating new db
    date_start = models.DateField(null=True)
    date_end = models.DateField(null=True)
    img = models.CharField(null=True)

    class Meta:
        ordering = ['name']


#---------------------------------
## POST
class Post(models.Model):
    title = models.CharField(max_length=50)
    time = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    label = models.CharField(choices=POST_LABELS)
    edited = models.BooleanField(default=False)

    #one-to-many relationship
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    festival = models.ForeignKey(Festival, on_delete=models.CASCADE, related_name='festival_posts')

    #many-to-many relationship
    post_liked_by = models.ManyToManyField(CustomUser, related_name='liked_posts')
    post_disliked_by = models.ManyToManyField(CustomUser, related_name='disliked_posts')

    class Meta:
        ordering = ['-time']


# also add comments
#---------------------------------
# COMMENTS
class Comment(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    edited = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)

    #one-to-many
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comments')

    #self reference
    parent = models.ForeignKey('self', null=True, blank=True, related_name='child_comments', on_delete=models.CASCADE)

    #many-to-many
    comment_liked_by = models.ManyToManyField(CustomUser, related_name='liked_comments')
    comment_disliked_by = models.ManyToManyField(CustomUser, related_name='disliked_comments')

    class Meta:
        ordering = ['-time']

#---------------------------------
#  CHAT

class Chat(models.Model):
    name = models.CharField(max_length=50)
    last_updated = models.DateTimeField(auto_now=True)

    # one-to-many relationship
    festival = models.ForeignKey(Festival, on_delete=models.CASCADE, related_name='festival_chat')

    # many-to-many
    notified_users = models.ManyToManyField(CustomUser, related_name='chat_notifications')


class Message(models.Model):
    text = models.TextField()
    time = models.DateTimeField(auto_now_add=True)

    # one-to-many relationship
    # TODO : maybe we will need to add related_name on author for list of his messages
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='chat_messages')

    class Meta:
        ordering = ['-time']


class Notification(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    # one-to-many
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
from email.policy import default
from django.db import models
from django.core import validators
from moviepy.editor import VideoFileClip
from django.core.exceptions import ValidationError

# Create your models here.

class videos(models.Model):
    caption = models.CharField(max_length=200)
    videoes = models.FileField(validators=[validators.FileExtensionValidator(allowed_extensions=['mp4','mkv'],message = 'Only mp4 and mkv videos are allowed!')])
    created = models.DateField(auto_now_add=True)
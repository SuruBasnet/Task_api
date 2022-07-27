from django.forms import ModelForm
from .models import videos

class Videosform(ModelForm):
    class Meta:
        model = videos
        fields = '__all__'
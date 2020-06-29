from django import forms
from .models import Media

class MediaFileUploadForm(forms.ModelForm):
    class Meta:
        model = Media
        fields = ('file',) 
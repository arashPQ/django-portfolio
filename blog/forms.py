from django import forms
from django.core.validators import FileExtensionValidator

from blog.models import Article


class ArticleForm(forms.ModelForm):
    
    image = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}), validators=[FileExtensionValidator])
    class Meta:
        model = Article
        fields = ['image']
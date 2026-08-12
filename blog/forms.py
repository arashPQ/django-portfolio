from django import forms
from django.core.validators import FileExtensionValidator

from blog.models import Article


class ArticleForm(forms.ModelForm):
    image = forms.FileField(
        widget=forms.FileInput(
            attrs={
                "class": "btn btn-info",
            }
        ),
        validators=[
            FileExtensionValidator(
                allowed_extensions=[
                    "jpg",
                    "jpeg",
                    "png",
                    "webp",
                ]
            )
        ],
    )

    class Meta:
        model = Article
        fields = ["image"]
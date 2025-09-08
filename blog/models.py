from django.db import models
from django.utils.text import slugify
from django.contrib.postgres.fields import JSONField


class Author(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.EmailField(max_length=64)
    phone = models.CharField(max_length=11)
    image = models.ImageField(upload_to='author/')
    address = models.CharField(max_length=128, blank=True, null=True)
    country = models.CharField(max_length=32, blank=True, null=True)
    state = models.CharField(max_length=32, blank=True, null=True)
    city = models.CharField(max_length=32, blank=True, null=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def name(self):
        return f'{self.first_name} {self.last_name}'


class Tags(models.Model):
    title = models.CharField(max_length=64)
    slug = models.SlugField(unique=True, default=title)
    description = models.CharField(max_length=128, null=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Article(models.Model):
    title = models.CharField(max_length=128)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, default=1)
    description = models.TextField(max_length=512)
    article = models.JSONField(blank=True, null=True)
    image = models.ImageField(upload_to='article/')
    tag = models.ManyToManyField(Tags, blank=True)
    slug = models.SlugField()
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class SubTitle(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    body = models.TextField(max_length=500000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title} from {self.article}'

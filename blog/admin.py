from django.contrib import admin

from blog.models import Author, Article, Tags, SubTitle


class SubTitleAdmin(admin.ModelAdmin):
    list_display = ('article', 'title', 'created_at', 'updated_at')


admin.site.register(Author)
admin.site.register(Article)
admin.site.register(Tags)
admin.site.register(SubTitle, SubTitleAdmin)
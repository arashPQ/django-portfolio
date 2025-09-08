from django.contrib import admin
from developer.models import Developer, Resume, Technology, Projects, ProjectImage


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1


@admin.register(Projects)
class ProjectAdmin(admin.ModelAdmin):
    inlines = [ProjectImageInline]
    


admin.site.register(Developer)
admin.site.register(Resume)
admin.site.register(Technology)
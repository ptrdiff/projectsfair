from django.contrib import admin
from .models import Project, Tag, Skill, Type, Profile


class SkillInline(admin.TabularInline):
    model = Project.skill.through
    extra = 0


class TagsInline(admin.TabularInline):
    model = Project.tag.through
    extra = 0


class ProjectAdmin(admin.ModelAdmin):
    list_display = ['project_name', 'pub_date', 'head', 'type']
    list_filter = ['head', 'type']
    fields = ['project_name', 'pub_date', ('start_date', 'end_date'), 'head', 'brief_summary', 'content', 'app_deadline',
              'num_places', 'type', 'members', 'status'
              ]
    inlines = [SkillInline, TagsInline]
    exclude = ['Skill', 'Tag']


admin.site.register(Project, ProjectAdmin)
admin.site.register(Skill)
admin.site.register(Tag)
admin.site.register(Type)
admin.site.register(Profile)

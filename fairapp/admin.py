from django.contrib import admin
from .models import Project, Skill, Profile, AppForProject, Education, EduInst, EduProg,\
    Activity, ApSkill, SciSkill, ExtSkill, ApAct, SciAct, ExtAct, ProjApSkill, ProjSciSkill,\
    ProjExtSkill, ProjApAct, ProjSciAct, ProjExtAct, Tag, Faculty, EduStage, EducationProfileRelation


'''class SkillInline(admin.TabularInline):
    model = Project.skill.through
    extra = 0
'''

class TagsInline(admin.TabularInline):
    model = Project.tag.through
    extra = 0


class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'date_start']
    # list_filter = ['head', 'type']
    # fields = ['project_name', 'pub_date', ('start_date', 'end_date'), 'head', 'brief_summary', 'content',
    #           'app_deadline', 'num_places', 'type', 'members', 'status'
    #           ]
    inlines = [TagsInline]
    exclude = ['Tag']


admin.site.register(Project)
admin.site.register(Skill)
admin.site.register(Tag)
admin.site.register(Profile)
admin.site.register(AppForProject)
admin.site.register(Education)
admin.site.register(EduInst)
admin.site.register(EduProg)
admin.site.register(Activity)
admin.site.register(ApSkill)
admin.site.register(SciSkill)
admin.site.register(ExtSkill)
admin.site.register(ApAct)
admin.site.register(SciAct)
admin.site.register(ExtAct)
admin.site.register(ProjApSkill)
admin.site.register(ProjSciSkill)
admin.site.register(ProjExtSkill)
admin.site.register(ProjApAct)
admin.site.register(ProjSciAct)
admin.site.register(ProjExtAct)
admin.site.register(Faculty)
admin.site.register(EduStage)
admin.site.register(EducationProfileRelation)

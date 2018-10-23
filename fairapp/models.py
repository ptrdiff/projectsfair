from datetime import date

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Type(models.Model):
    type_name = models.CharField(max_length=255)

    def __str__(self):
        return self.type_name


class Tag(models.Model):
    tag_name = models.CharField(max_length=255)

    def __str__(self):
        return self.tag_name


'''class Skill(models.Model):
    skill_name = models.CharField(max_length=255)

    def __str__(self):
        return self.skill_name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    interests = models.CharField(max_length=1000)
    achievements = models.CharField(max_length=1000)
    FACULTY = (
        ('a', 'ApMath'),
        ('c', 'Chemistry'),
        ('p', 'Physics'),
        ('m', 'MathMech'),
        ('b', 'Biology'),
        ('l', 'Faculty of Law'),
        ('s', 'Social Faculty'),
    )
    faculty = models.CharField(max_length=1, choices=FACULTY, blank=True, help_text='Faculty')

    STATUS = (
        ('b', 'Bachelor'),
        ('m', 'Master'),
        ('g', 'Graduate Student'),
        ('t', 'Teacher'),
    )
    status = models.CharField(max_length=1, choices=STATUS, blank=True, help_text='Status')

    grade = models.PositiveIntegerField(blank=True, null=True, )

    def __str__(self):
        return self.user.username
'''

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


'''class Project(models.Model):
    project_name = models.CharField(max_length=255)
    pub_date = models.DateField('date published', default=date.today)
    start_date = models.DateField('starting date', default=date.today)
    end_date = models.DateField('ending date', default=date.today)
    head = models.ManyToManyField(User, related_name='head')
    brief_summary = models.TextField(max_length=1000)
    content = models.TextField(max_length=2000)
    app_deadline = models.DateField('application deadline', default=date.today)
    num_places = models.PositiveIntegerField(default=1)
    type = models.ForeignKey(Type, null=True, blank=True, on_delete=models.CASCADE)
    skill = models.ManyToManyField(Skill, related_name='skills')
    tag = models.ManyToManyField(Tag, related_name='tags')
    members = models.ManyToManyField(User, related_name='members', blank=True)
    PROJECT_STATUS = (
        ('m', 'Moderation'),
        ('c', 'Collecting participants'),
        ('p', 'In progress'),
        ('f', 'Finished'),
        ('r', 'Rejected'),
    )
    status = models.CharField(max_length=1, choices=PROJECT_STATUS, blank=True, default='m', help_text='Project status')

    class Meta:
        permissions = (
            ("approve_project", "Can approve project"),
            ("reject_project", "Can reject project"),
        )

    def __str__(self):
        return self.project_name

    def get_absolute_url(self):
        return "/%i/" % self.id
'''


#=========================================================================


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    mname = models.CharField(null=False, blank = True, max_length=255, help_text="Middle name")
    phone = models.CharField(null=False, blank = True, max_length=32, help_text="Phone number")


class EduInst(models.Model):
    name = models.CharField(null=False, blank=False, max_length=255, help_text="Institute name")


class EduProg(models.Model):
    name = models.CharField(null=False, blank=False, max_length=255, help_text="Program name")


class Education(models.Model):
    id_user = models.OneToOneField(Profile, on_delete=models.CASCADE)
    id_edu = models.OneToOneField(EduInst, on_delete=models.CASCADE)
    id_prog = models.OneToOneField(EduProg, on_delete=models.CASCADE)
    year = models.PositiveIntegerField(help_text="Graduation year")


class Skill(models.Model):
    name = models.CharField(null=False, blank=False, max_length=255, help_text="Skill name", default="")


class Activities(models.Model):
    name = models.CharField(null=False, blank=False, max_length=255, help_text="Activity name")


class ApSkills(models.Model):
    id_user = models.OneToOneField(Profile, on_delete=models.CASCADE)
    id_skill = models.OneToOneField(Skill, on_delete=models.CASCADE)


class SciSkills(models.Model):
    id_user = models.OneToOneField(Profile, on_delete=models.CASCADE)
    id_skill = models.OneToOneField(Skill, on_delete=models.CASCADE)


class ExtSkills(models.Model):
    id_user = models.OneToOneField(Profile, on_delete=models.CASCADE)
    id_skill = models.OneToOneField(Skill, on_delete=models.CASCADE)


class ApAct(models.Model):
    id_user = models.OneToOneField(Profile, on_delete=models.CASCADE)
    id_act = models.OneToOneField(Activities, on_delete=models.CASCADE)


class SciAct(models.Model):
    id_user = models.OneToOneField(Profile, on_delete=models.CASCADE)
    id_act = models.OneToOneField(Activities, on_delete=models.CASCADE)


class ExtAct(models.Model):
    id_user = models.OneToOneField(Profile, on_delete=models.CASCADE)
    id_act = models.OneToOneField(Activities, on_delete=models.CASCADE)


class Project(models.Model):
    name = models.CharField(null=False, blank=False, max_length=255, help_text="Institute name", default="")
    id_lead = models.OneToOneField(Profile, on_delete=models.CASCADE, default=0)
    descrip_short = models.TextField(blank=False, max_length=1024, default="")
    descrip_full = models.TextField(blank=False, max_length=8192, default="")
    num_participants = models.PositiveSmallIntegerField(help_text="Full number of places", default=0)
    places_left = models.PositiveSmallIntegerField(help_text="Number of left places", default=0)
    date_start = models.DateField("Date of project start", default=date.today)
    date_end = models.DateField("Date of project end", default=date.today)
    date_req_end = models.DateField("Deadline for applications", default=date.today)


class ProjApSkills(models.Model):
    id_proj = models.OneToOneField(Project, on_delete=models.CASCADE)
    id_skill = models.OneToOneField(Skill, on_delete=models.CASCADE)


class ProjSciSkills(models.Model):
    id_proj = models.OneToOneField(Project, on_delete=models.CASCADE)
    id_skill = models.OneToOneField(Skill, on_delete=models.CASCADE)


class ProjExtSkills(models.Model):
    id_proj = models.OneToOneField(Project, on_delete=models.CASCADE)
    id_skill = models.OneToOneField(Skill, on_delete=models.CASCADE)


class ProjApAct(models.Model):
    id_proj = models.OneToOneField(Project, on_delete=models.CASCADE)
    id_act = models.OneToOneField(Activities, on_delete=models.CASCADE)


class ProjSciAct(models.Model):
    id_proj = models.OneToOneField(Project, on_delete=models.CASCADE)
    id_act = models.OneToOneField(Activities, on_delete=models.CASCADE)


class ProjExtAct(models.Model):
    id_proj = models.OneToOneField(Project, on_delete=models.CASCADE)
    id_act = models.OneToOneField(Activities, on_delete=models.CASCADE)


class UserProject(models.Model):
    id_user = models.OneToOneField(Profile, on_delete=models.CASCADE)
    id_proj = models.OneToOneField(Project, on_delete=models.CASCADE)
    is_lead = models.BooleanField(default=False)
#=========================================================================



class AppForProject(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    covering_letter = models.TextField(max_length=1000)
    APPLICATION_STATUS = (
        ('m', 'Moderation'),
        ('a', 'Approved'),
        ('r', 'Rejected'),
    )
    status = models.CharField(max_length=1, choices=APPLICATION_STATUS, blank=True, default='m',
                              help_text='Application status')

    class Meta:
        permissions = (
            ("approve_application", "Can approve application"),
            ("reject_application", "Can reject application"),
        )
        unique_together = ('project', 'user')
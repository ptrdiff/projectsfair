from datetime import date

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.db import models


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Tag(models.Model):
    name = models.CharField(null=False, blank=False, max_length=255, help_text="Tag name", default="")

    def __str__(self):
        return self.name


class EduInst(models.Model):
    name = models.CharField(null=False, blank=False, max_length=255, help_text="Institute name")

    def __str__(self):
        return self.name


class EduProg(models.Model):
    name = models.CharField(null=False, blank=False, max_length=255, help_text="Program name")

    def __str__(self):
        return self.name


class Faculty(models.Model):
    name = models.CharField(null=False, blank=False, max_length=255, help_text="Faculty name")

    def __str__(self):
        return self.name


class EduStage(models.Model):
    name = models.CharField(null=False, blank=False, max_length=255, help_text="Education stage")

    def __str__(self):
        return self.name


class Education(models.Model):
    edu = models.ForeignKey(EduInst, on_delete=models.CASCADE,       related_name='edu')
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE,   related_name='faculty')
    prog = models.ForeignKey(EduProg, on_delete=models.CASCADE,      related_name='prog')
    stage = models.ForeignKey(EduStage, on_delete=models.CASCADE,    related_name='stage')
    year = models.PositiveIntegerField(help_text="Graduation year", default=int(date.today().year))

    def __str__(self):
        return str(self.edu.__str__() + " " + self.prog.__str__() + " " + self.year.__str__())


class Skill(models.Model):
    name = models.CharField(null=False, blank=False, max_length=255, help_text="Skill name", default="")

    def __str__(self):
        return self.name


class Activity(models.Model):
    name = models.CharField(null=False, blank=False, max_length=255, help_text="Activity name")

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    middle_name = models.CharField(null=False, blank=True, max_length=255, help_text="Middle name")
    phone = models.CharField(null=False, blank=True, max_length=32, help_text="Phone number")
    education = models.ManyToManyField(Education, default=0, related_name="education", through="EducationProfileRelation")
    ap_skill = models.ManyToManyField(Skill, default=0, related_name="ap_skill", through="ApSkill", through_fields=('user', 'skill'))
    sci_skill = models.ManyToManyField(Skill, default=0, related_name="sci_skill", through="SciSkill",through_fields=('user', 'skill'))
    ext_skill = models.ManyToManyField(Skill, default=0, related_name="ext_skill", through="ExtSkill",through_fields=('user', 'skill'))
    ap_act = models.ManyToManyField(Activity, default=0, related_name="ap_act",through="ApAct")
    sci_act = models.ManyToManyField(Activity, default=0, related_name="sci_act",through="SciAct")
    ext_act = models.ManyToManyField(Activity, default=0, related_name="ext_act",through="ExtAct")

    def __str__(self):
        return self.user.username


class EducationProfileRelation(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    education = models.ForeignKey(Education, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.__str__() + " " + self.education.__str__()


class ApSkill(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)

    def __str__(self):
        return self.skill.__str__()


class SciSkill(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)

    def __str__(self):
        return self.skill.__str__()


class ExtSkill(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)

    def __str__(self):
        return self.skill.__str__()


class ApAct(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    act = models.ForeignKey(Activity, on_delete=models.CASCADE)

    def __str__(self):
        return self.act.__str__()


class SciAct(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    act = models.ForeignKey(Activity, on_delete=models.CASCADE)

    def __str__(self):
        return self.act.__str__()


class ExtAct(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    act = models.ForeignKey(Activity, on_delete=models.CASCADE)

    def __str__(self):
        return self.act.__str__()


class Project(models.Model):
    name = models.TextField(null=False, blank=False, max_length=255, help_text="Institute name", default="")
    id_lead = models.ManyToManyField(User, related_name="id_lead")
    descrip_short = models.TextField(blank=False, max_length=1024, default="")
    descrip_full = models.TextField(blank=False, max_length=8192, default="")
    num_participants = models.PositiveSmallIntegerField(help_text="Full number of places", default=5)
    places_left = models.PositiveSmallIntegerField(help_text="Number of left places", default=0)
    date_start = models.DateField("Date of project start", default=date.today)
    date_end = models.DateField("Date of project end", default=date.today)
    date_req_end = models.DateField("Deadline for applications", default=date.today)
    tag = models.ManyToManyField(Tag, related_name='Tags')
    skill = models.ManyToManyField(Skill, related_name='Skills')
    activity = models.ManyToManyField(Activity, related_name='Activities')
    members = models.ManyToManyField(User, related_name='members', blank=True)

    PROJECT_STATUS = (
        ('m', 'Moderation'),
        ('c', 'Collecting participants'),
        ('p', 'In progress'),
        ('f', 'Finished'),
        ('r', 'Rejected'),
    )
    status = models.CharField(max_length=1, choices=PROJECT_STATUS, blank=True, default='m', help_text='Project status')

    def __str__(self):
        return self.name

    class Meta:
        permissions = (
            ("approve_project", "Can approve project"),
            ("reject_project", "Can reject project"),
        )

    def get_absolute_url(self):
        return "/%i/" % self.id


class ProjApSkill(models.Model):
    proj = models.ManyToManyField(Project, default=0)
    skill = models.ManyToManyField(Skill, default=0)

    def __str__(self):
        return self.skill.__str__()


class ProjSciSkill(models.Model):
    proj = models.ManyToManyField(Project, default=0)
    skill = models.ManyToManyField(Skill, default=0)

    def __str__(self):
        return self.skill.__str__()


class ProjExtSkill(models.Model):
    proj = models.ManyToManyField(Project, default=0)
    skill = models.ManyToManyField(Skill, default=0)

    def __str__(self):
        return self.skill.__str__()


class ProjApAct(models.Model):
    proj = models.ManyToManyField(Project, default=0)
    act = models.ManyToManyField(Activity, default=0)

    def __str__(self):
        return self.act.__str__()


class ProjSciAct(models.Model):
    proj = models.ManyToManyField(Project, default=0)
    act = models.ManyToManyField(Activity, default=0)

    def __str__(self):
        return self.act.__str__()


class ProjExtAct(models.Model):
    proj = models.ManyToManyField(Project, default=0)
    act = models.ManyToManyField(Activity, default=0)

    def __str__(self):
        return self.act.__str__()


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

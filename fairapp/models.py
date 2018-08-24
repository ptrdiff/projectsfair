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


class Skill(models.Model):
    skill_name = models.CharField(max_length=255)

    def __str__(self):
        return self.skill_name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    interests = models.TextField(max_length=1000)
    achievements = models.TextField(max_length=1000)
    FACULTY = (
        ('a', 'ApMath'),
        ('c', 'Chemistry'),
        ('p', 'Physics'),
        ('m', 'MathMech'),
        ('b', 'Biology'),
        ('l', 'Faculty of Law'),
        ('s', 'Social Faculty'),
    )
    faculty = models.CharField(max_length=1, choices=FACULTY, blank=True, default=1, help_text='Faculty')

    STATUS = (
        ('b', 'Bachelor'),
        ('m', 'Master'),
        ('g', 'Graduate Student'),
        ('t', 'Teacher'),
    )
    status = models.CharField(max_length=1, choices=STATUS, blank=True, default=1, help_text='Status')

    grade = models.PositiveIntegerField(blank=True, null=True, )

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Project(models.Model):
    project_name = models.TextField(max_length=255)
    pub_date = models.DateTimeField('date published', default=timezone.now)
    start_date = models.DateTimeField('starting date', default=timezone.now)
    end_date = models.DateTimeField('ending date', default=timezone.now)
    head = models.ManyToManyField(User, related_name='head')
    brief_summary = models.TextField(max_length=1000)
    content = models.TextField(max_length=1000)
    app_deadline = models.DateTimeField('application deadline', default=timezone.now)
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
    status = models.CharField(max_length=1, choices=PROJECT_STATUS, blank=True, default=1, help_text='Project status')

    class Meta:
        permissions = (
            ("approve_project", "Can approve project"),
            ("reject_project", "Can reject project"),
        )

    def __str__(self):
        return self.project_name

    def get_absolute_url(self):
        return "/%i/" % self.id




class AppForProject(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    covering_letter = models.TextField(max_length=1000)
    APPLICATION_STATUS = (
        ('m', 'Moderation'),
        ('a', 'Approved'),
        ('r', 'Rejected'),
    )
    status = models.CharField(max_length=1, choices=APPLICATION_STATUS, blank=True, default=1, help_text='Application '
                                                                                                         'status')

    class Meta:
        permissions = (
            ("approve_application", "Can approve application"),
            ("reject_application", "Can reject application"),
        )



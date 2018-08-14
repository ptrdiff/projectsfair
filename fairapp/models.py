from django.db import models
from django.urls import reverse


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


class Project(models.Model):
    project_name = models.TextField(max_length=255)
    pub_date = models.DateTimeField('date published')
    start_date = models.DateTimeField('starting date')
    end_date = models.DateTimeField('ending date')
    head = models.TextField(max_length=255)
    brief_summary = models.TextField(max_length=1000)
    content = models.TextField(max_length=1000)
    app_deadline = models.DateTimeField('application deadline')
    num_places = models.PositiveIntegerField()
    type = models.ForeignKey(Type, null=True, blank=True, on_delete=models.CASCADE)
    skill = models.ManyToManyField(Skill, related_name='skills')
    tag = models.ManyToManyField(Tag, related_name='tags')

    def __str__(self):
        return self.project_name

    def get_absolute_url(self):
        """
        Returns the url to access a particular book instance.
        """
        return reverse('', args=[str(self.id)])

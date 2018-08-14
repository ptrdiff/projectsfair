from django.db import models


#model type

#model tags

#model skills


class Project(models.Model):
    project_name = models.CharField(max_length=255)
    pub_date = models.DateTimeField('date published')
    start_date = models.DateTimeField('starting date')
    end_date = models.DateTimeField('ending date')
    head = models.CharField(max_length=255)
    brief_summary = models.CharField(max_length=1000)
    content = models.CharField(max_length=1000)
    type = models.CharField(max_length=255) #
    app_deadline = models.DateTimeField('application deadline')
    num_places = models.PositiveIntegerField()
    required_skills = models.CharField(max_length=255) #
    tags = models.CharField(max_length=255) #

    def __str__(self):
        return self.project_name

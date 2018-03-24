from django.db import models

# Create your models here.


class Subtitles(models.Model):
	id = models.AutoField(primary_key=True)
	filename = models.CharField(max_length=70, blank=False)
	text = models.CharField(max_length=100000, blank=False)


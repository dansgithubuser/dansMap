from django.contrib.auth.models import User
from django.db import models

class Note(models.Model):
	text=models.TextField()
	created=models.DateTimeField()
	user=models.ForeignKey(User, models.CASCADE)

from django.contrib.auth.models import User
from django.db import models

class Note(models.Model):
	text=models.TextField()
	latitude=models.DecimalField(9, 6)
	longitude=models.DecimalField(9, 6)
	created=models.DateTimeField(auto_now_add=True)
	user=models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True)

	def __str__(self):
		return '{} {} {}'.format(self.created, self.user, self.text[:40])

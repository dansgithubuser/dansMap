from django.contrib.auth.models import User
from django.db import models

class Note(models.Model):
	text=models.TextField()
	latitude=models.DecimalField(max_digits=9, decimal_places=6, default=0)
	longitude=models.DecimalField(max_digits=9, decimal_places=6, default=0)
	created=models.DateTimeField(auto_now_add=True)
	user=models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True)

	def __str__(self):
		return '{} {} ({}, {}) {}'.format(self.created, self.user, self.latitude, self.longitude, self.text[:40])

	def to_dict(self):
		def simplify(x):
			if x is None: return None
			return str(x)
		return {i: simplify(getattr(self, i)) for i in ['text', 'latitude', 'longitude', 'created', 'user']}

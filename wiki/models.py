import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Text(models.Model):
	body = models.CharField(max_length=5000)
	
	def __str__(self):
		return self.body
		
	pass
	
class Revision(models.Model):
	text = models.ForeignKey(Text)
	date = models.DateTimeField('date modified')
	log = models.CharField(max_length=100)
	user = models.ForeignKey(User)
	
	def __str__(self):
		return self.date.strftime('%c')
		
	def was_recent_revision(self):
		return self.date >= timezone.now() - datetime.timedelta(days=1)
		
	pass
	

class Article(models.Model):
	title = models.CharField(max_length=50)
	date = models.DateTimeField('date created')
	latest = models.ForeignKey(Revision, related_name='+')
	creator = models.ForeignKey(User)
	revisions = models.ManyToManyField(Revision, related_name='Article')
	path = models.SlugField(max_length=40)
	
	def __str__(self):
		return self.title

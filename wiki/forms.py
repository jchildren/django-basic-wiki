from django import forms
from django.forms import ModelForm, Textarea

from .models import Article, Revision, Text

class ArticleForm(ModelForm):
	class Meta:
		model = Article
		fields = ['title']
		
class RevisionForm(ModelForm):
	class Meta:
		model = Revision
		fields = ['log']
		
class TextForm(ModelForm):
	class Meta:
		model = Text
		fields = ['body']
		widgets = {
            'body': Textarea(attrs={'cols': 80, 'rows': 20}),
        }
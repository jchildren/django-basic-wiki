import datetime

from django.utils import timezone

from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.views import generic

from django.contrib.auth.models import User

from .models import Article, Revision, Text
from .forms import ArticleForm, RevisionForm, TextForm
    
class IndexView(generic.ListView):
    template_name = 'pages/index.html'
    context_object_name = 'articles_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Article.objects.order_by('-date')[:5]

class ArticleView(generic.DetailView):
    model = Article
    template_name = 'pages/article.html'
     
def EditView(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
        
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        article_form = ArticleForm(request.POST)
        revision_form = RevisionForm(request.POST)
        text_form = TextForm(request.POST)
        
        # check whether it's valid:
        if revision_form.is_valid() and text_form.is_valid():
        
            # Creates a new text object with the form input
            text = Text(body=text_form.cleaned_data['body'])
            text.save()
            
            #TODO: correctly access user
            user = User.objects.get(id=1)
            
            # Creates a new revision with the updated text
            revision = Revision(text=text, date=timezone.now(), log=revision_form.cleaned_data['log'], user=user)
            revision.save()
        
            article.latest = revision
            article.revisions.add(revision)
            article.save()
            
            # process the data in form.cleaned_data as required
            # Always return an HttpResponseRedirect after successfully dealing
            # with POST data. This prevents data from being posted twice if a
            # user hits the Back button.
            return HttpResponseRedirect(reverse('wiki:article', args=(article.id,)))
        else:
            return render(request, 'pages/article.html', {'article': article})

    # if a GET (or any other method) we'll create a blank form
    else:
        article_form = ArticleForm(instance=article)
        revision_form = RevisionForm()
        text_form = TextForm(instance=article.latest.text)
        
        return render(request, 'pages/edit.html', 
        {'article': article,
         'article_form': article_form,
         'revision_form': revision_form,
         'text_form': text_form,
         })

def RevisionsView(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    return render(request, 'pages/revisions.html', {'article': article})
    
def RevertView(request, article_id, revision_id):
    article = get_object_or_404(Article, pk=article_id)
    revision = get_object_or_404(Revision, pk=revision_id)
    
    if article.latest.text == revision.text:
        # TODO: Display an error
        error_message = 'Target revision identical to current'
        
        return HttpResponseRedirect(reverse('wiki:revisions', args=(article.id,)))
    
    else:
        # Default log message for reversion
        log_message = 'Reverted to ' + revision.date.strftime('%c')
    
        user = User.objects.get(id=1)
        user.save()
    
        new_revision = Revision(text=revision.text, date=timezone.now(), log=log_message, user=user)
        new_revision.save()
        
        article.latest = new_revision
        article.save()
        article.revisions.add(new_revision)
    
        return HttpResponseRedirect(reverse('wiki:revisions', args=(article.id,)))
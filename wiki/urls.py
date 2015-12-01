from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    # ex: /wiki/5/
    url(r'^(?P<pk>[0-9]+)/$', views.ArticleView.as_view(), name='article'),
    # ex: /wiki/5/edit/
    url(r'^(?P<article_id>[0-9]+)/edit/$', views.EditView, name='edit'),
    # ex: /wiki/5/revisions/
    url(r'^(?P<article_id>[0-9]+)/revisions/$', views.RevisionsView, name='revisions'),
    # ex: /wiki/5/revert/2
    url(r'^(?P<article_id>[0-9]+)/revert/(?P<revision_id>[0-9]+)/$', views.RevertView, name='revert'),
]

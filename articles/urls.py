from django.urls import path

from articles import views

urlpatterns = [
    path('', views.index),
    path('<int:article_id>/like/', views.like_article, name='like_article'),
    path('<int:article_id>/', views.article_by_id, name='article_by_id'),
    # path('<slug:article_name>/', views.article_by_name, name='article_by_name'),
    path('search/', views.search, name='article_search')
]

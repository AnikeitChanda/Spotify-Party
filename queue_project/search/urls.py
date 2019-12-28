from django.urls import path
from . import views

urlpatterns = [
    path('', views.search_home, name = 'search-home'),
    path('confirmation/', views.confirmation, name = 'confirmation-home'),
    path('skip/', views.skip_song, name = 'skip-home'),
]
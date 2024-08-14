from django.urls import path
from .views import scoreboard, issues_view, pull_request_list, home

urlpatterns = [
    path('scoreboard/', scoreboard, name='scoreboard'),
    path('', home, name='home'),
    path('issues/', issues_view, name='issues_view'),
    path('pr/', pull_request_list, name='pull_request_list'),
]

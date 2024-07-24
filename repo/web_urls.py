from django.urls import path
from .views import scoreboard, issues_view, pull_request_list

urlpatterns = [
    path('', scoreboard, name='scoreboard'),
    path('issues/', issues_view, name='issues_view'),
    path('pr/', pull_request_list, name='pull_request_list'),
]

from django.shortcuts import render
from rest_framework import viewsets
from .models import Contributor, Issue, PullRequest, Score
from .serializers import ContributorSerializer, IssueSerializer, PullRequestSerializer, ScoreSerializer

def scoreboard(request):
    scores = Score.objects.select_related('contributor').prefetch_related('badges').order_by('rank')
    return render(request, 'scoreboard.html', {'scores': scores})

def home(request):
    return render(request, 'home.html')

def issues_view(request):
    issues = Issue.objects.select_related('contributor').all()
    return render(request, 'issues.html', {'issues': issues})

def pull_request_list(request):
    pull_requests = PullRequest.objects.all()
    return render(request, 'pull_requests.html', {'pull_requests': pull_requests})

class ContributorViewSet(viewsets.ModelViewSet):
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer

class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer

class PullRequestViewSet(viewsets.ModelViewSet):
    queryset = PullRequest.objects.all()
    serializer_class = PullRequestSerializer

class ScoreViewSet(viewsets.ModelViewSet):
    queryset = Score.objects.select_related('contributor').prefetch_related('badges').order_by('rank')
    serializer_class = ScoreSerializer

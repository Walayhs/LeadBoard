from django.urls import path
from .views import ContributorViewSet, IssueViewSet, PullRequestViewSet, ScoreViewSet, pull_request_list
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'contributors', ContributorViewSet)
router.register(r'issues', IssueViewSet)
router.register(r'pull_requests', PullRequestViewSet)
router.register(r'scoreboard', ScoreViewSet)

urlpatterns = router.urls
urlpatterns += [
    path('pull-requests/', pull_request_list, name='pull_request_list'),
]

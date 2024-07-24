from rest_framework import serializers
from .models import Contributor, Issue, PullRequest, Score, Badge

class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = '__all__'

class BadgeSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Badge
        fields = ['id', 'name', 'image_url']

    def get_image_url(self, obj):
        return obj.image_url

class IssueSerializer(serializers.ModelSerializer):
    contributor = ContributorSerializer()
    class Meta:
        model = Issue
        fields = '__all__'

class PullRequestSerializer(serializers.ModelSerializer):
    contributor = ContributorSerializer()
    labels = serializers.JSONField()
    class Meta:
        model = PullRequest
        fields = '__all__'

class ScoreSerializer(serializers.ModelSerializer):
    contributor = ContributorSerializer()  # Nested Contributor data
    badges = BadgeSerializer(many=True)  # Nested list of Badge data

    class Meta:
        model = Score
        fields = ['id', 'rank', 'username', 'score', 'contributor', 'badges']

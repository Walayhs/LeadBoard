from django.db import models

class Badge(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='badges/', default='badges/default_badge.jpg')

    @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        return '/media/badges/default_badge.jpg'

    def __str__(self):
        return self.name

class Contributor(models.Model):
    username = models.CharField(max_length=100)
    github_id = models.IntegerField(unique=True)
    avatar_url = models.URLField(max_length=200)
    badges = models.ManyToManyField(Badge, blank=True)

    def __str__(self):
        return self.username

class Score(models.Model):
    contributor = models.ForeignKey(Contributor, on_delete=models.CASCADE)
    username = models.CharField(max_length=100)
    score = models.IntegerField()
    rank = models.IntegerField()
    total_prs = models.IntegerField(default=0)
    badges = models.ManyToManyField(Badge, blank=True)

    def __str__(self):
        return f'{self.rank}: {self.username} - {self.score}'

class Issue(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    issue_id = models.BigIntegerField(unique=True, blank=True, default=None)
    state = models.CharField(max_length=50)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    url = models.URLField()
    contributor = models.ForeignKey(Contributor, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class PullRequest(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    pr_id = models.BigIntegerField(unique=True, blank=True, default=None)
    state = models.CharField(max_length=50)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    merged_at = models.DateTimeField(null=True, blank=True)
    url = models.URLField()
    labels = models.JSONField(default=list)
    contributor = models.ForeignKey(Contributor, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

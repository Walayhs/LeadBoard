from django.core.management.base import BaseCommand
from repo.models import Contributor, Issue, PullRequest, Score, Badge
from datetime import datetime
import pytz
import requests
import os

class Command(BaseCommand):
    help = 'Fetch data from GitHub and save it to the database'

    def handle(self, *args, **kwargs):
        headers = {'Authorization': f'token {os.getenv("GITHUB_TOKEN")}'}
        repo_owner = os.getenv("REPO_OWNER")
        repo_name = os.getenv("REPO_NAME")

        # Fetch Issues
        self.fetch_and_save_issues(repo_owner, repo_name, headers)

        # Fetch Pull Requests
        self.fetch_and_save_pull_requests(repo_owner, repo_name, headers)

        # Fetch Comments
        # self.fetch_and_save_comments(repo_owner, repo_name, headers)

        # Calculate Scores within the specified date range
        self.calculate_scores()

    def fetch_and_save_issues(self, repo_owner, repo_name, headers):
        url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/issues'
        params = {
            "state": "all",
            "per_page": 100,
            "page": 1
        }
        issues = []
        while True:
            response = requests.get(url, headers=headers, params=params)
            if response.status_code != 200:
                print(f'Issues Status Code: {response.status_code}')
                print('Issues Response:', response.json())
                break

            data = response.json()
            if not data:
                break
            issues.extend(data)
            params["page"] += 1

        for issue in issues:
            contributor_data = issue['user']
            contributor, created = Contributor.objects.update_or_create(
                username=contributor_data['login'],
                github_id=contributor_data['id'],
                defaults={'avatar_url': contributor_data['avatar_url']}
            )
            Issue.objects.update_or_create(
                issue_id=issue['id'],
                defaults={
                    'title': issue['title'],
                    'state': issue['state'],
                    'created_at': issue['created_at'],
                    'updated_at': issue['updated_at'],
                    'url': issue['html_url'],
                    'contributor': contributor
                }
            )

    def fetch_and_save_pull_requests(self, repo_owner, repo_name, headers):
        url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/pulls'
        params = {
            "state": "all",
            "per_page": 100,
            "page": 1
        }
        prs = []
        while True:
            response = requests.get(url, headers=headers, params=params)
            if response.status_code != 200:
                print(f'PRs Status Code: {response.status_code}')
                print('PRs Response:', response.json())
                break

            data = response.json()
            if not data:
                break
            prs.extend(data)
            params["page"] += 1

        for pr in prs:
            contributor_data = pr['user']
            contributor, created = Contributor.objects.update_or_create(
                username=contributor_data['login'],
                github_id=contributor_data['id'],
                defaults={'avatar_url': contributor_data['avatar_url']}
            )
            PullRequest.objects.update_or_create(
                pr_id=pr['id'],
                defaults={
                    'title': pr['title'],
                    'state': pr['state'],
                    'created_at': pr['created_at'],
                    'updated_at': pr['updated_at'],
                    'url': pr['html_url'],
                    'contributor': contributor,
                    'labels': pr['labels']  # Save labels
                }
            )

    # def fetch_and_save_comments(self, repo_owner, repo_name, headers):
    #     url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/issues/comments'
    #     params = {
    #         "per_page": 100,
    #         "page": 1
    #     }
    #     comments = []
    #     while True:
    #         response = requests.get(url, headers=headers, params=params)
    #         if response.status_code != 200:
    #             print(f'Comments Status Code: {response.status_code}')
    #             print('Comments Response:', response.json())
    #             break

    #         data = response.json()
    #         if not data:
    #             break
    #         comments.extend(data)
    #         params["page"] += 1

    #     for comment in comments:
    #         issue = None
    #         pr = None

    #         issue_url = comment.get('issue_url')
    #         if issue_url:
    #             issue_id = issue_url.split('/')[-1]
    #             if issue_id.isdigit():
    #                 issue = Issue.objects.filter(issue_id=issue_id).first()

    #         pr_url = comment.get('pull_request_url')
    #         if pr_url:
    #             pr_id = pr_url.split('/')[-1]
    #             if pr_id.isdigit():
    #                 pr = PullRequest.objects.filter(pr_id=pr_id).first()

            
            

    def calculate_scores(self):
        LEVEL_POINTS = {
            'LEVEL-1': 10,
            'LEVEL-2': 20,
            'LEVEL-3': 30
        }

        start_date = datetime(2023, 7, 20, tzinfo=pytz.utc)
        end_date = datetime(2023, 8, 20, tzinfo=pytz.utc)
        exclude_usernames = [
            'tinawankhede', 'Shlokwankhade', 'CLOUDyy003', 'Tejaswinipaunikar',
            'rohansnishad', 'sanskruti-kokde', 'animex007', 'Walayhs', 
            'Axwell-2', 'lukey2207', 'Anjali0903', 'Surajh09', 'jitacm'
        ]
        contributors = Contributor.objects.exclude(username__in=exclude_usernames)

        Score.objects.all().delete()  # Clear previous scores

        scores = []
        contributor_scores = []

        for contributor in contributors:
            score = 0
            prs = PullRequest.objects.filter(contributor=contributor, created_at__range=(start_date, end_date))

            for pr in prs:
                for label in pr.labels:
                    score += LEVEL_POINTS.get(label['name'], 0)

            contributor_scores.append({
                'contributor': contributor,
                'score': score
            })                       

        # Sort scores in descending order
        ranked_contributors = sorted(contributor_scores, key=lambda x: x['score'], reverse=True)

        # Create Score records with rank
        for rank, entry in enumerate(ranked_contributors, start=1):
            # Determine badges based on conditions
            badges = []
            if entry['score'] >= 100:
                badges.append({
                    'name': 'PullChampion',
                    'image_url': 'https://github.com/Walayhs/GitBot/blob/main/Badges/pullchampion.jpg'
                })
            if len(PullRequest.objects.filter(contributor=entry['contributor'], created_at__range=(start_date, end_date))) > 5:
                badges.append({
                    'name': '30DaysDevChallenge',
                    'image_url': 'https://github.com/Walayhs/GitBot/blob/main/Badges/30daysdevchallenge.jpg'
                },
                badges.append({
                    'name': 'OpenSourceContributor',
                    'image_url': 'https://github.com/Walayhs/GitBot/blob/main/Badges/opensrccontributor.jpg'
                },)
                )

            Score.objects.create(
                rank=rank,
                username=entry['contributor'].username,
                score=entry['score'],
                contributor=entry['contributor'],
                badges=badges  # Add badge data
            )

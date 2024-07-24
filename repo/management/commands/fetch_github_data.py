import requests
import os
from django.core.management.base import BaseCommand
from repo.models import Contributor, Issue, PullRequest, Score, Badge
from dotenv import load_dotenv
from datetime import datetime
from django.utils import timezone
from tqdm import tqdm
import pytz
from django.db import transaction

load_dotenv()

class Command(BaseCommand):
    help = 'Fetch data from GitHub and save it to the database'

    def handle(self, *args, **kwargs):
        headers = {'Authorization': f'token {os.getenv("GITHUB_TOKEN")}'}
        repo_owner = os.getenv("REPO_OWNER")
        repo_name = os.getenv("REPO_NAME")

        # Fetch Issues and Pull Requests
        self.fetch_data(repo_owner, repo_name, headers)

        # Calculate Scores
        self.calculate_scores()

    @transaction.atomic
    def fetch_data(self, repo_owner, repo_name, headers):
        self.fetch_and_save_issues(repo_owner, repo_name, headers)
        self.fetch_and_save_pull_requests(repo_owner, repo_name, headers)

    def fetch_and_save_issues(self, repo_owner, repo_name, headers):
        url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/issues'
        params = {"state": "all", "per_page": 100, "page": 1}
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

        self.save_issues(issues)

    @transaction.atomic
    def save_issues(self, issues):
        issue_objs = []
        contributor_objs = []
        for issue in tqdm(issues, desc="Saving Issues", unit="issue"):
            contributor_data = issue['user']
            contributor, created = Contributor.objects.get_or_create(
                github_id=contributor_data['id'],
                defaults={'username': contributor_data['login'], 'avatar_url': contributor_data['avatar_url']}
            )
            if not created and (contributor.username != contributor_data['login'] or contributor.avatar_url != contributor_data['avatar_url']):
                contributor.username = contributor_data['login']
                contributor.avatar_url = contributor_data['avatar_url']
                contributor.save()
            issue_objs.append(
                Issue(
                    issue_id=issue['id'],
                    title=issue['title'],
                    state=issue['state'],
                    created_at=issue['created_at'],
                    updated_at=issue['updated_at'],
                    url=issue['html_url'],
                    contributor=contributor
                )
            )
        Issue.objects.bulk_create(issue_objs, ignore_conflicts=True)

    def fetch_and_save_pull_requests(self, repo_owner, repo_name, headers):
        url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/pulls'
        params = {"state": "all", "per_page": 100, "page": 1}
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

        self.save_pull_requests(prs)

    @transaction.atomic
    def save_pull_requests(self, prs):
        pr_objs = []
        for pr in tqdm(prs, desc="Saving Pull Requests", unit="pr"):
            contributor_data = pr['user']
            contributor, created = Contributor.objects.get_or_create(
                github_id=contributor_data['id'],
                defaults={'username': contributor_data['login'], 'avatar_url': contributor_data['avatar_url']}
            )
            if not created and (contributor.username != contributor_data['login'] or contributor.avatar_url != contributor_data['avatar_url']):
                contributor.username = contributor_data['login']
                contributor.avatar_url = contributor_data['avatar_url']
                contributor.save()
            pr_objs.append(
                PullRequest(
                    pr_id=pr['id'],
                    title=pr['title'],
                    state=pr['state'],
                    merged_at=pr.get('merged_at'),
                    created_at=pr['created_at'],
                    updated_at=pr['updated_at'],
                    url=pr['html_url'],
                    contributor=contributor,
                    labels=pr['labels']
                )
            )
        PullRequest.objects.bulk_create(pr_objs, ignore_conflicts=True)

    @transaction.atomic
    def calculate_scores(self):
        LEVEL_POINTS = {
            'LEVEL-1': 10,
            'LEVEL-2': 20,
            'LEVEL-3': 30
        }
        exclude_usernames = [
            'tinawankhede','CLOUDyy003', 'Tejaswinipaunikar',
            'rohansnishad', 'sanskruti-kokde', 'Walayhs', 
            'Axwell-2', 'lukey2207', 'Anjali0903', 'Surajh09','jitacm',
        ]
        contributors = Contributor.objects.exclude(username__in=exclude_usernames)
        
        contributor_scores = []
        start_date = datetime(2024, 7, 20, tzinfo=pytz.utc)
        end_date = datetime(2024, 8, 20, tzinfo=pytz.utc)
        
        for contributor in tqdm(contributors, desc="Calculating Scores", unit="contributor"):
            score = 0
            prs = PullRequest.objects.filter(contributor=contributor, created_at__range=(start_date, end_date))
            merged_prs = prs.filter(state='closed', merged_at__isnull=False)
            issues = Issue.objects.filter(contributor=contributor, created_at__range=(start_date, end_date))

            for pr in prs:
                for label in pr.labels:
                    score += LEVEL_POINTS.get(label['name'], 0)

            contributor_scores.append({
                'contributor': contributor,
                'score': score,
                'num_prs': prs.count(),
                'num_merged_prs': merged_prs.count(),
                'num_issues': issues.count()
            })

        self.rank_contributors(contributor_scores)

    @transaction.atomic
    def rank_contributors(self, contributor_scores):
        ranked_contributors = sorted(contributor_scores, key=lambda x: x['score'], reverse=True)
        badges = {
            'dev_challenge': Badge.objects.get_or_create(name='30DaysDevChallenge', defaults={'image': 'badges/30daysdevchallenge.png'})[0],
            'pull_master': Badge.objects.get_or_create(name='PullMaster', defaults={'image': 'badges/PullMaster.png'})[0],
            'opensource_contrib': Badge.objects.get_or_create(name='OpenSourceContributor', defaults={'image': 'badges/OpenSourceContributor.png'})[0],
            'pull_champion': Badge.objects.get_or_create(name='PullChampion', defaults={'image': 'badges/PullChampion.png'})[0],
            'opensource_adventurer': Badge.objects.get_or_create(name='OpenSourceAdventurer', defaults={'image': 'badges/OpenSourceAdventurer.png'})[0],
            'tech_trailblazer': Badge.objects.get_or_create(name='TechTrailblazer', defaults={'image': 'badges/TechTrailblazer.png'})[0]
        }
        score_entries = []
        for rank, entry in tqdm(enumerate(ranked_contributors, start=1), desc="Creating Score Entries", unit="score"):
            badges_to_assign = []
            # Apply badge logic here if needed
            
            score_entry, created = Score.objects.update_or_create(
                rank=rank,
                username=entry['contributor'].username,
                defaults={'score': entry['score'], 'contributor': entry['contributor'], 'total_prs': entry['num_prs']}
            )
            score_entry.badges.set(badges_to_assign)

            score_entries.append(score_entry)

        Score.objects.bulk_update(score_entries, ['score', 'contributor', 'total_prs'])

# repo/tasks.py
import os
from celery import shared_task
from .management.commands.fetch_github_data import Command

@shared_task
def fetch_github_contributions():
    command = Command()
    command.handle()

@shared_task
def fetch_latest_issues_prs():
    command = Command()
    headers = {'Authorization': f'token {os.getenv("GITHUB_TOKEN")}'}
    repo_owner = os.getenv("REPO_OWNER")
    repo_name = os.getenv("REPO_NAME")
    command.fetch_and_save_issues(repo_owner, repo_name, headers)
    command.fetch_and_save_pull_requests(repo_owner, repo_name, headers)

# # your_app/management/commands/create_badges.py

# from django.core.management.base import BaseCommand
# from repo.models import Badge

# class Command(BaseCommand):
#     help = 'Create default badges'

#     def handle(self, *args, **kwargs):
#         badges = [
#             {'name': '30DaysDevChallenge', 'image_url': 'https://github.com/Walayhs/GitBot/blob/main/Badges/30daysdevchallenge.jpg'},
#             {'name': 'OpenSourceAdventurer', 'image_url': 'https://github.com/Walayhs/GitBot/blob/main/Badges/opensrcadventurer.jpg'},
#             {'name': 'OpenSourceContributor', 'image_url': 'https://github.com/Walayhs/GitBot/blob/main/Badges/opensrccontributor.jpg'},
#             {'name': 'PullChampion', 'image_url': 'https://github.com/Walayhs/GitBot/blob/main/Badges/pullchampion.jpg'},
#             {'name': 'PullMaster', 'image_url': 'https://github.com/Walayhs/GitBot/blob/main/Badges/pullmaster.jpg'},
#             {'name': 'TechTrailblazer', 'image_url': 'https://github.com/Walayhs/GitBot/blob/main/Badges/techtrailblazer.jpg'}
#         ]

#         for badge_data in badges:
#             badge, created = Badge.objects.get_or_create(name=badge_data['name'], defaults=badge_data)
#             if created:
#                 self.stdout.write(self.style.SUCCESS(f'Badge "{badge.name}" created successfully.'))
#             else:
#                 self.stdout.write(self.style.WARNING(f'Badge "{badge.name}" already exists.'))

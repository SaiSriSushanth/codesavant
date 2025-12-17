import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'code_assistant_platform.settings')
django.setup()

from coding_assistant.models import Badge

badges = [
    {
        'name': 'First Snippet',
        'description': 'Created your first code snippet',
        'icon': 'fas fa-code',
        'criteria': 'first_snippet',
        'xp_bonus': 50
    },
    {
        'name': '10 Likes',
        'description': 'Received 10 likes on your snippets',
        'icon': 'fas fa-heart',
        'criteria': '10_likes',
        'xp_bonus': 100
    },
    {
        'name': 'First Comment',
        'description': 'Posted your first comment',
        'icon': 'fas fa-comment',
        'criteria': 'first_comment',
        'xp_bonus': 25
    },
    {
        'name': 'Prolific Coder',
        'description': 'Created 5 code snippets',
        'icon': 'fas fa-layer-group',
        'criteria': '5_snippets',
        'xp_bonus': 150
    }
]

for badge_data in badges:
    badge, created = Badge.objects.get_or_create(
        name=badge_data['name'],
        defaults=badge_data
    )
    if created:
        print(f"Created badge: {badge.name}")
    else:
        print(f"Badge already exists: {badge.name}")

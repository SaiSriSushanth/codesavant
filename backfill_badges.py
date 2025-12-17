import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'code_assistant_platform.settings')
django.setup()

from django.contrib.auth.models import User
from coding_assistant.utils import check_badges, get_or_create_profile

def backfill_badges():
    users = User.objects.all()
    print(f"Checking badges for {users.count()} users...")
    
    for user in users:
        print(f"Processing user: {user.username}")
        # Ensure profile exists
        get_or_create_profile(user)
        # Check and award badges
        check_badges(user)
        
    print("Backfill complete!")

if __name__ == '__main__':
    backfill_badges()

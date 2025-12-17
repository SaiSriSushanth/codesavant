from .models import UserProfile, Badge, CodeSnippet, Comment, UserBadge

def get_or_create_profile(user):
    profile, created = UserProfile.objects.get_or_create(user=user)
    return profile

def calculate_level(xp):
    # Simple level formula: Level = 1 + (XP / 100)
    return 1 + (xp // 100)

def award_xp(user, amount):
    profile = get_or_create_profile(user)
    profile.xp += amount
    
    # Check for level up
    new_level = calculate_level(profile.xp)
    if new_level > profile.level:
        profile.level = new_level
        # Could add notification logic here
        
    profile.save()
    check_badges(user)
    return profile

def check_badges(user):
    profile = get_or_create_profile(user)
    badges = Badge.objects.all()
    
    for badge in badges:
        if UserBadge.objects.filter(profile=profile, badge=badge).exists():
            continue
            
        awarded = False
        if badge.criteria == 'first_snippet':
            if CodeSnippet.objects.filter(user=user).exists():
                awarded = True
        elif badge.criteria == '10_likes':
            total_likes = sum(snippet.likes.count() for snippet in CodeSnippet.objects.filter(user=user))
            if total_likes >= 10:
                awarded = True
        elif badge.criteria == 'first_comment':
            if Comment.objects.filter(user=user).exists():
                awarded = True
        elif badge.criteria == '5_snippets':
            if CodeSnippet.objects.filter(user=user).count() >= 5:
                awarded = True
                
        if awarded:
            UserBadge.objects.create(profile=profile, badge=badge)
            if badge.xp_bonus > 0:
                award_xp(user, badge.xp_bonus)
            # Could add notification logic here

from django.db import models
from django.contrib.auth.models import User

class CodeSnippet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='code_snippets')
    title = models.CharField(max_length=200)
    code = models.TextField()
    language = models.CharField(max_length=50)
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

class AIFeedback(models.Model):
    code_snippet = models.ForeignKey(CodeSnippet, on_delete=models.CASCADE, related_name='ai_feedbacks')
    feedback = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Feedback for {self.code_snippet.title}"

class LearningResource(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    url = models.URLField()
    resource_type = models.CharField(max_length=50, choices=[
        ('TUTORIAL', 'Tutorial'),
        ('DOCUMENTATION', 'Documentation'),
        ('EXERCISE', 'Exercise'),
        ('VIDEO', 'Video'),
        ('ARTICLE', 'Article'),
    ])
    tags = models.CharField(max_length=200)  # Comma-separated tags
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progress')
    skill = models.CharField(max_length=100)  # e.g., "Python", "JavaScript", "Algorithms"
    proficiency_level = models.IntegerField(default=1)  # 1-10 scale
    last_activity = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('user', 'skill')
    
    def __str__(self):
        return f"{self.user.username}'s {self.skill} progress"

class CodingChallenge(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    difficulty = models.CharField(max_length=20, choices=[
        ('BEGINNER', 'Beginner'),
        ('INTERMEDIATE', 'Intermediate'),
        ('ADVANCED', 'Advanced'),
    ])
    starter_code = models.TextField(blank=True)
    solution = models.TextField()
    tags = models.CharField(max_length=200)  # Comma-separated tags
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class Comment(models.Model):
    code_snippet = models.ForeignKey(CodeSnippet, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Comment by {self.user.username} on {self.code_snippet.title}"

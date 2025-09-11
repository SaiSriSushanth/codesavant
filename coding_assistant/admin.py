from django.contrib import admin
from .models import CodeSnippet, AIFeedback, LearningResource, UserProgress, CodingChallenge, Comment

# Register your models here.
@admin.register(CodeSnippet)
class CodeSnippetAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'language', 'is_public', 'created_at')
    list_filter = ('language', 'is_public', 'created_at')
    search_fields = ('title', 'user__username')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(AIFeedback)
class AIFeedbackAdmin(admin.ModelAdmin):
    list_display = ('code_snippet', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('code_snippet__title',)
    readonly_fields = ('created_at',)

@admin.register(LearningResource)
class LearningResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'resource_type', 'created_at')
    list_filter = ('resource_type', 'created_at')
    search_fields = ('title', 'tags')
    readonly_fields = ('created_at',)

@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'skill', 'proficiency_level', 'last_activity')
    list_filter = ('skill', 'proficiency_level', 'last_activity')
    search_fields = ('user__username', 'skill')
    readonly_fields = ('last_activity',)

@admin.register(CodingChallenge)
class CodingChallengeAdmin(admin.ModelAdmin):
    list_display = ('title', 'difficulty', 'created_at')
    list_filter = ('difficulty', 'created_at')
    search_fields = ('title', 'tags')
    readonly_fields = ('created_at',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('code_snippet', 'user', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('code_snippet__title', 'user__username', 'content')
    readonly_fields = ('created_at', 'updated_at')

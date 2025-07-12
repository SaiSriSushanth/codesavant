from django.urls import path
from . import views

app_name = 'coding_assistant'

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('code-editor/', views.code_editor, name='code_editor'),
    path('api/analyze-code/', views.analyze_code, name='analyze_code'),
    path('api/run-code/', views.run_code, name='run_code'),
    path('api/learning-resources/', views.get_learning_resources, name='learning_resources'),
    path('api/coding-challenge/', views.get_coding_challenge, name='coding_challenge'),
    path('snippet/<int:snippet_id>/', views.view_snippet, name='view_snippet'),
    path('explore/', views.explore, name='explore'),
    path('public-snippet/<int:snippet_id>/', views.public_snippet, name='public_snippet'),
    path('api/add-comment/', views.add_comment, name='add_comment'),
    path('api/toggle-public/', views.toggle_public, name='toggle_public'),
    path('api/save-snippet/', views.save_snippet, name='save_snippet'),
]
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import CodeSnippet, AIFeedback, LearningResource, UserProgress, CodingChallenge, Comment
import openai
import json
import subprocess
import tempfile
import os
import sys
import traceback
import re

# Remove global API key initialization as we'll use client-based approach
# openai.api_key = settings.OPENAI_API_KEY

def index(request):
    """Home page view"""
    return render(request, 'coding_assistant/index.html')

@login_required
def dashboard(request):
    """User dashboard view"""
    user_snippets = CodeSnippet.objects.filter(user=request.user).order_by('-created_at')
    user_progress = UserProgress.objects.filter(user=request.user)
    
    context = {
        'snippets': user_snippets,
        'progress': user_progress,
    }
    return render(request, 'coding_assistant/dashboard.html', context)

@login_required
def code_editor(request):
    """Code editor view"""
    return render(request, 'coding_assistant/code_editor.html')

@csrf_exempt
def analyze_code(request):
    """API endpoint to analyze code with GPT-4"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            code = data.get('code', '')
            language = data.get('language', 'python')
            action = data.get('action', 'analyze')  # analyze, optimize, explain, etc.
            
            if not code:
                return JsonResponse({'error': 'No code provided'}, status=400)
            
            # Create or update code snippet if user is authenticated
            if request.user.is_authenticated:
                title = data.get('title', f"{language} snippet")
                snippet, created = CodeSnippet.objects.get_or_create(
                    user=request.user,
                    title=title,
                    defaults={'code': code, 'language': language}
                )
                
                if not created:
                    snippet.code = code
                    snippet.language = language
                    snippet.save()
            
            # Prepare prompt based on action
            prompts = {
                'analyze': f"Analyze this {language} code and provide feedback on code quality, potential bugs, and suggestions for improvement:\n\n```{language}\n{code}\n```",
                'optimize': f"Optimize this {language} code for better performance and readability. Explain your changes:\n\n```{language}\n{code}\n```",
                'explain': f"Explain this {language} code in detail, breaking down how it works and what each part does:\n\n```{language}\n{code}\n```",
                'debug': f"Debug this {language} code. Identify and fix any errors or potential issues:\n\n```{language}\n{code}\n```",
                'challenge': f"Based on this {language} code, suggest a related coding challenge that would help improve skills:\n\n```{language}\n{code}\n```"
            }
            
            prompt = prompts.get(action, prompts['analyze'])
            
            # Call OpenAI API - Updated for OpenAI API v1.90.0
            client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
            response = client.chat.completions.create(
                model=settings.GPT_MODEL,
                messages=[
                    {"role": "system", "content": "You are an expert programming tutor and code reviewer. Provide detailed, educational feedback that helps the developer learn and improve their coding skills."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500,
                temperature=0.7,
            )
            
            # Extract response - Updated for OpenAI API v1.90.0
            ai_response = response.choices[0].message.content
            
            # Save feedback if user is authenticated
            if request.user.is_authenticated:
                AIFeedback.objects.create(
                    code_snippet=snippet,
                    feedback=ai_response
                )
                
                # Update user progress based on code analysis
                update_user_progress(request.user, language, code, ai_response)        
            
            return JsonResponse({
                'feedback': ai_response,
                'snippet_id': snippet.id if request.user.is_authenticated else None
            })
            
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

def update_user_progress(user, language, code, feedback):
    """Update user progress based on code analysis"""
    # Simple algorithm to update user proficiency
    # In a real app, this would be more sophisticated
    progress, created = UserProgress.objects.get_or_create(
        user=user,
        skill=language,
        defaults={'proficiency_level': 1}
    )
    
    # Very basic proficiency update logic
    # In a real app, you'd use NLP or more sophisticated analysis
    if 'excellent' in feedback.lower() or 'great job' in feedback.lower():
        if progress.proficiency_level < 10:
            progress.proficiency_level += 1
            progress.save()
    
    return progress

@csrf_exempt
def run_code(request):
    """API endpoint to run code in a sandboxed environment"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            code = data.get('code', '')
            language = data.get('language', 'python')
            
            if not code:
                return JsonResponse({'error': 'No code provided'}, status=400)
            
            # Execute the code based on language
            output, error = execute_code(code, language)
            
            # Return the result
            return JsonResponse({
                'output': output,
                'error': error
            })
            
        except Exception as e:
            print(traceback.format_exc())
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

def execute_code(code, language):
    """Execute code in a sandboxed environment with improved error handling"""
    output = ''
    error = ''
    temp_file_path = None
    
    try:
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=get_file_extension(language)) as temp_file:
            temp_file.write(code.encode('utf-8'))
            temp_file_path = temp_file.name
        
        # Execute the code based on language
        if language == 'python':
            # Run Python code
            try:
                # First check for syntax errors
                compile(code, '<string>', 'exec')
                
                process = subprocess.Popen(
                    [sys.executable, temp_file_path],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                stdout, stderr = process.communicate(timeout=5)  # 5 second timeout for safety
                
                if process.returncode != 0:
                    error = format_error_message(stderr, language, code)
                else:
                    output = stdout
                    if stderr:
                        error = format_error_message(stderr, language, code)
            except SyntaxError as e:
                error = f"Syntax Error: {str(e)}"
                line_num = e.lineno if hasattr(e, 'lineno') else 0
                if line_num > 0:
                    code_lines = code.split('\n')
                    if line_num <= len(code_lines):
                        error += f"\nLine {line_num}: {code_lines[line_num-1]}"
                    else:
                        error += f"\nLine {line_num}: (line not found)"
            
        elif language == 'javascript':
            # Run JavaScript with Node.js
            process = subprocess.Popen(
                ['node', temp_file_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            stdout, stderr = process.communicate(timeout=5)  # 5 second timeout for safety
            
            if process.returncode != 0:
                error = format_error_message(stderr, language, code)
            else:
                output = stdout
                if stderr:
                    error = format_error_message(stderr, language, code)
        
        elif language == 'ruby':
            # Run Ruby code
            process = subprocess.Popen(
                ['ruby', temp_file_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            stdout, stderr = process.communicate(timeout=5)
            
            if process.returncode != 0:
                error = format_error_message(stderr, language, code)
            else:
                output = stdout
                if stderr:
                    error = format_error_message(stderr, language, code)
        
        elif language == 'php':
            # Run PHP code
            process = subprocess.Popen(
                ['php', temp_file_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            stdout, stderr = process.communicate(timeout=5)
            
            if process.returncode != 0:
                error = format_error_message(stderr, language, code)
            else:
                output = stdout
                if stderr:
                    error = format_error_message(stderr, language, code)
        
        else:
            # For unsupported languages, return an error
            error = f"Language '{language}' is not supported for execution yet. Supported languages: Python, JavaScript, Ruby, PHP"
    
    except subprocess.TimeoutExpired:
        error = "Execution timed out. Your code took too long to run (limit: 5 seconds)."
    except FileNotFoundError as e:
        if 'node' in str(e):
            error = "Node.js is not installed or not in PATH. Please install Node.js to run JavaScript code."
        elif 'ruby' in str(e):
            error = "Ruby is not installed or not in PATH. Please install Ruby to run Ruby code."
        elif 'php' in str(e):
            error = "PHP is not installed or not in PATH. Please install PHP to run PHP code."
        else:
            error = f"Required interpreter not found: {str(e)}"
    except PermissionError:
        error = "Permission denied when trying to execute the code. Please check your system permissions."
    except Exception as e:
        error = f"Error executing code: {str(e)}"
    finally:
        # Clean up the temporary file
        if temp_file_path:
            try:
                os.unlink(temp_file_path)
            except:
                pass
    
    return output, error

def format_error_message(error_text, language, code):
    """Format error messages to be more user-friendly and include line numbers"""
    if not error_text:
        return ""
    
    # Split code into lines for reference
    code_lines = code.split('\n')
    
    if language == 'python':
        # Extract line numbers from Python errors
        if 'line ' in error_text:
            try:
                # Find line numbers in the error message
                line_matches = re.findall(r'line (\d+)', error_text)
                if line_matches:
                    line_num = int(line_matches[0])
                    if 1 <= line_num <= len(code_lines):
                        # Add the code line to the error message
                        error_parts = error_text.split('\n')
                        for i, part in enumerate(error_parts):
                            if f'line {line_num}' in part:
                                error_parts.insert(i+1, f"Code: {code_lines[line_num-1].strip()}")
                                break
                        return '\n'.join(error_parts)
            except:
                pass  # If parsing fails, return the original error
    
    elif language == 'javascript':
        # Format JavaScript errors
        if '.js:' in error_text:
            try:
                # Extract line and column information
                match = re.search(r'(\w+\.js):(\d+)(?::(\d+))?', error_text)
                if match:
                    line_num = int(match.group(2))
                    if 1 <= line_num <= len(code_lines):
                        # Add the code line to the error message
                        error_parts = error_text.split('\n')
                        for i, part in enumerate(error_parts):
                            if match.group(0) in part:
                                error_parts.insert(i+1, f"Code: {code_lines[line_num-1].strip()}")
                                break
                        return '\n'.join(error_parts)
            except:
                pass
    
    # For other languages or if specific formatting fails, return the original error
    return error_text

def get_file_extension(language):
    """Get file extension for a given language"""
    extensions = {
        'python': '.py',
        'javascript': '.js',
        'java': '.java',
        'cpp': '.cpp',
        'csharp': '.cs',
        'php': '.php',
        'ruby': '.rb',
        'go': '.go',
        'swift': '.swift',
        'kotlin': '.kt'
    }
    return extensions.get(language, '.txt')

@login_required
def get_learning_resources(request):
    """API endpoint to get personalized learning resources"""
    language = request.GET.get('language', '')
    skill_level = 'beginner'  # Default
    
    # Get user's proficiency level if available
    try:
        progress = UserProgress.objects.get(user=request.user, skill=language)
        level = progress.proficiency_level
        
        if level <= 3:
            skill_level = 'beginner'
        elif level <= 7:
            skill_level = 'intermediate'
        else:
            skill_level = 'advanced'
    except UserProgress.DoesNotExist:
        pass
    
    # Query for resources or generate with AI if none exist
    resources = LearningResource.objects.filter(
        tags__contains=language
    ).filter(
        tags__contains=skill_level
    )[:5]
    
    if not resources:
        # Generate resources with AI
        try:
            prompt = f"Suggest 3 learning resources for {skill_level} {language} developers. For each resource, provide a title, brief description, and URL. Format as JSON."
            
            # Updated for OpenAI API v1.90.0
            client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
            response = client.chat.completions.create(
                model=settings.GPT_MODEL,
                messages=[
                    {"role": "system", "content": "You are an expert programming educator who knows the best learning resources."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.7,
            )
            
            ai_response = response.choices[0].message.content
            
            # Parse JSON from response (in a real app, add more error handling)
            try:
                # Extract JSON from markdown if needed
                if '```json' in ai_response:
                    ai_response = ai_response.split('```json')[1].split('```')[0].strip()
                
                resources_data = json.loads(ai_response)
                
                # Save resources to database
                for resource in resources_data:
                    LearningResource.objects.create(
                        title=resource.get('title', ''),
                        description=resource.get('description', ''),
                        url=resource.get('url', ''),
                        resource_type='ARTICLE',  # Default
                        tags=f"{language},{skill_level}"
                    )
                
                # Query again
                resources = LearningResource.objects.filter(
                    tags__contains=language
                ).filter(
                    tags__contains=skill_level
                )[:5]
                
            except json.JSONDecodeError:
                # Handle non-JSON response
                pass
                
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    # Serialize resources
    resources_list = [{
        'id': r.id,
        'title': r.title,
        'description': r.description,
        'url': r.url,
        'type': r.resource_type
    } for r in resources]
    
    return JsonResponse({'resources': resources_list})

@login_required
def get_coding_challenge(request):
    """Get a personalized coding challenge"""
    language = request.GET.get('language', 'python')
    
    # Determine difficulty based on user progress
    difficulty = 'BEGINNER'  # Default
    try:
        progress = UserProgress.objects.get(user=request.user, skill=language)
        level = progress.proficiency_level
        
        if level <= 3:
            difficulty = 'BEGINNER'
        elif level <= 7:
            difficulty = 'INTERMEDIATE'
        else:
            difficulty = 'ADVANCED'
    except UserProgress.DoesNotExist:
        difficulty = 'BEGINNER'  # Default for new users
    
    # Check if we have a suitable challenge in the database
    existing_challenges = CodingChallenge.objects.filter(
        difficulty=difficulty,
        tags__contains=language
    ).order_by('?')[:1]  # Random selection
    
    if existing_challenges.exists():
        challenge = existing_challenges.first()
    else:
        # Generate a challenge with AI
        try:
            prompt = f"Create a {difficulty.lower()} level coding challenge for {language}. Include a title, description, starter code, and solution. Format as JSON."
            
            # Updated for OpenAI API v1.90.0
            client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
            response = client.chat.completions.create(
                model=settings.GPT_MODEL,
                messages=[
                    {"role": "system", "content": "You are an expert programming educator who creates engaging coding challenges."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500,
                temperature=0.8,
            )
            
            ai_response = response.choices[0].message.content
            
            # Parse JSON from response
            try:
                # Extract JSON from markdown if needed
                if '```json' in ai_response:
                    ai_response = ai_response.split('```json')[1].split('```')[0].strip()
                    
                challenge_data = json.loads(ai_response)
                
                # Save challenge to database
                challenge = CodingChallenge.objects.create(
                    title=challenge_data.get('title', ''),
                    description=challenge_data.get('description', ''),
                    difficulty=difficulty,
                    starter_code=challenge_data.get('starter_code', ''),
                    solution=challenge_data.get('solution', ''),
                    tags=f"{language},{difficulty.lower()}"
                )
                
            except json.JSONDecodeError:
                return JsonResponse({'error': 'Failed to generate challenge'}, status=500)
                
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    # Return challenge data
    challenge_data = {
        'id': challenge.id,
        'title': challenge.title,
        'description': challenge.description,
        'starter_code': challenge.starter_code,
        'difficulty': challenge.difficulty,
    }
    
    return JsonResponse({'challenge': challenge_data})

@login_required
def view_snippet(request, snippet_id):
    """View a specific code snippet and its feedback"""
    snippet = get_object_or_404(CodeSnippet, id=snippet_id, user=request.user)
    feedbacks = snippet.ai_feedbacks.all().order_by('-created_at')
    
    context = {
        'snippet': snippet,
        'feedbacks': feedbacks,
    }
    
    return render(request, 'coding_assistant/view_snippet.html', context)

def explore(request):
    """Explore public code snippets"""
    public_snippets = CodeSnippet.objects.filter(is_public=True).order_by('-created_at')
    
    # Filter by language if specified
    language = request.GET.get('language')
    if language:
        public_snippets = public_snippets.filter(language=language)
    
    # Get unique languages for filter dropdown
    languages = CodeSnippet.objects.filter(is_public=True).values_list('language', flat=True).distinct()
    
    context = {
        'snippets': public_snippets,
        'languages': languages,
        'selected_language': language,
    }
    
    return render(request, 'coding_assistant/explore.html', context)

def public_snippet(request, snippet_id):
    """View a public code snippet with comments"""
    snippet = get_object_or_404(CodeSnippet, id=snippet_id, is_public=True)
    comments = snippet.comments.all().order_by('-created_at')
    
    context = {
        'snippet': snippet,
        'comments': comments,
    }
    
    return render(request, 'coding_assistant/public_snippet.html', context)

@login_required
@csrf_exempt
def add_comment(request):
    """API endpoint to add a comment to a public snippet"""
    if request.method == 'POST':
        try:
            # Log request information for debugging
            print(f"Request method: {request.method}")
            print(f"Request headers: {request.headers}")
            print(f"Request body: {request.body}")
            
            try:
                data = json.loads(request.body)
                print(f"Parsed data: {data}")
                snippet_id = data.get('snippet_id')
                content = data.get('content')
                
                print(f"Snippet ID: {snippet_id}, Content: {content}")
                
                if not snippet_id or not content:
                    print("Missing required fields")
                    return JsonResponse({'error': 'Missing required fields', 'received': data}, status=400)
                
                # Verify the snippet exists and is public
                try:
                    snippet = get_object_or_404(CodeSnippet, id=snippet_id, is_public=True)
                    print(f"Found snippet: {snippet.title}")
                except Exception as snippet_error:
                    print(f"Snippet error: {str(snippet_error)}")
                    return JsonResponse({'error': f'Snippet error: {str(snippet_error)}'}, status=404)
                
                # Create the comment
                comment = Comment.objects.create(
                    code_snippet=snippet,
                    user=request.user,
                    content=content
                )
                print(f"Created comment: {comment.id}")
                
                return JsonResponse({
                    'success': True,
                    'comment': {
                        'id': comment.id,
                        'content': comment.content,
                        'user': comment.user.username,
                        'created_at': comment.created_at.strftime('%B %d, %Y, %I:%M %p')
                    }
                })
            except json.JSONDecodeError as json_error:
                print(f"JSON decode error: {str(json_error)}")
                return JsonResponse({'error': f'Invalid JSON: {str(json_error)}'}, status=400)
            
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)
    else:
        print(f"Invalid method: {request.method}")
        return JsonResponse({'error': 'Only POST method is allowed'}, status=405)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@login_required
@csrf_exempt
def toggle_public(request):
    """API endpoint to toggle a snippet's public status"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            snippet_id = data.get('snippet_id')
            
            if not snippet_id:
                return JsonResponse({'error': 'Missing snippet ID'}, status=400)
            
            # Verify the user owns the snippet
            snippet = get_object_or_404(CodeSnippet, id=snippet_id, user=request.user)
            
            # Toggle the public status
            snippet.is_public = not snippet.is_public
            snippet.save()
            
            return JsonResponse({
                'success': True,
                'is_public': snippet.is_public
            })
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@login_required
@csrf_exempt
def save_snippet(request):
    """API endpoint to save a code snippet"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            code = data.get('code', '')
            title = data.get('title', 'Untitled Snippet')
            language = data.get('language', 'python')
            
            if not code:
                return JsonResponse({'error': 'No code provided'}, status=400)
            
            # Create or update code snippet
            snippet, created = CodeSnippet.objects.get_or_create(
                user=request.user,
                title=title,
                defaults={'code': code, 'language': language}
            )
            
            if not created:
                snippet.code = code
                snippet.language = language
                snippet.save()
            
            return JsonResponse({
                'success': True,
                'snippet_id': snippet.id,
                'message': 'Code snippet saved successfully'
            })
            
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

import os

explore_content = """{% extends 'base.html' %}

{% block title %}Explore Code Snippets - CodeSavant{% endblock %}

{% block content %}
<div class="row mb-4">
    <div class="col-12">
        <h1 class="mb-4">Explore Code Snippets</h1>
        <p class="lead">Discover and learn from public code snippets shared by the community</p>
    </div>
</div>

<div class="row mb-4">
    <div class="col-12">
        <div class="card shadow-sm">
            <div class="card-header bg-white">
                <div class="d-flex justify-content-between align-items-center">
                    <h4 class="mb-0">Filter Snippets</h4>
                    <a href="{% url 'coding_assistant:explore' %}" class="btn btn-sm btn-outline-secondary">Clear Filters</a>
                </div>
            </div>
            <div class="card-body">
                <form method="get" action="{% url 'coding_assistant:explore' %}" class="row g-3">
                    <div class="col-md-6">
                        <label for="q" class="form-label">Search</label>
                        <div class="input-group">
                            <span class="input-group-text"><i class="fas fa-search"></i></span>
                            <input type="text" name="q" id="q" class="form-control" placeholder="Search snippets..." value="{{ query|default:'' }}">
                        </div>
                    </div>
                    <div class="col-md-3">
                        <label for="language" class="form-label">Language</label>
                        <select name="language" id="language" class="form-select">
                            <option value="">All Languages</option>
                            {% for lang in languages %}
                            <option value="{{ lang }}" {% if selected_language == lang %}selected{% endif %}>{{ lang|title }}</option>
                            {% endfor %}
                        </select>
                    </div>
                    <div class="col-md-3">
                        <label for="sort" class="form-label">Sort By</label>
                        <select name="sort" id="sort" class="form-select">
                            <option value="latest" {% if sort == 'latest' %}selected{% endif %}>Newest First</option>
                            <option value="oldest" {% if sort == 'oldest' %}selected{% endif %}>Oldest First</option>
                            <option value="most_liked" {% if sort == 'most_liked' %}selected{% endif %}>Most Liked</option>
                        </select>
                    </div>
                    <div class="col-12 text-end">
                        <button type="submit" class="btn btn-primary">Apply Filters</button>
                        <a href="{% url 'coding_assistant:explore' %}" class="btn btn-outline-secondary">Clear</a>
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>

<div class="row">
    {% if snippets %}
    {% for snippet in snippets %}
    <div class="col-md-6 col-lg-4 mb-4">
        <div class="card h-100 shadow-sm">
            <div class="card-header bg-white">
                <div class="d-flex justify-content-between align-items-center">
                    <h5 class="mb-0 text-truncate" title="{{ snippet.title }}">{{ snippet.title }}</h5>
                    <span class="badge bg-secondary">{{ snippet.language }}</span>
                </div>
            </div>
            <div class="card-body">
                <p class="card-text text-muted small mb-2">
                    By <a href="{% url 'coding_assistant:user_profile' snippet.user.username %}" class="text-decoration-none">{{ snippet.user.username }}</a> 
                    on {{ snippet.created_at|date:"M d, Y" }}
                    {% if snippet.parent_snippet %}
                    <br>
                    <i class="fas fa-code-branch me-1 text-muted"></i> Forked
                    {% endif %}
                </p>
                <div class="code-preview mb-3">
                    <pre class="bg-light p-2 rounded"><code>{{ snippet.code|truncatechars:150 }}</code></pre>
                </div>
                <div class="d-flex justify-content-between align-items-center">
                    <div>
                        <span class="text-muted small me-2" title="Comments"><i class="far fa-comment me-1"></i>{{ snippet.comments.count }}</span>
                        <span class="text-muted small" title="Likes"><i class="far fa-heart me-1"></i>{{ snippet.likes.count }}</span>
                    </div>
                    <a href="{% url 'coding_assistant:public_snippet' snippet.id %}" class="btn btn-sm btn-primary">View Details</a>
                </div>
            </div>
        </div>
    </div>
    {% endfor %}
    {% else %}
    <div class="col-12">
        <div class="alert alert-info text-center">
            <p class="mb-0">No public snippets available yet. Be the first to share your code!</p>
        </div>
    </div>
    {% endif %}
</div>

{% if user.is_authenticated %}
<div class="row mt-4">
    <div class="col-12 text-center">
        <div class="card shadow-sm">
            <div class="card-body">
                <h5>Want to share your own code?</h5>
                <p>You can make your code snippets public from your dashboard or when viewing a specific snippet.</p>
                <a href="{% url 'coding_assistant:dashboard' %}" class="btn btn-primary">Go to Dashboard</a>
            </div>
        </div>
    </div>
</div>
{% endif %}
{% endblock %}

{% block extra_css %}
<style>
    .code-preview {
        max-height: 150px;
        overflow: hidden;
    }
    .code-preview pre {
        margin-bottom: 0;
        font-size: 0.8rem;
    }
</style>
{% endblock %}
"""

challenges_content = """{% extends 'base.html' %}

{% block title %}Coding Challenges - CodeSavant{% endblock %}

{% block content %}
<div class="row mb-4">
    <div class="col-12 text-center">
        <h1 class="mb-3">Coding Challenges Arena ⚔️</h1>
        <p class="lead">Test your skills, solve problems, and earn XP!</p>
    </div>
</div>

<div class="row mb-4">
    <div class="col-12">
        <div class="card shadow-sm">
            <div class="card-body">
                <form method="get" class="row g-3 align-items-center justify-content-center">
                    <div class="col-auto">
                        <label class="col-form-label fw-bold">Filter by:</label>
                    </div>
                    <div class="col-auto">
                        <select name="difficulty" class="form-select">
                            <option value="">All Difficulties</option>
                            <option value="BEGINNER" {% if selected_difficulty == 'BEGINNER' %}selected{% endif %}>Beginner</option>
                            <option value="INTERMEDIATE" {% if selected_difficulty == 'INTERMEDIATE' %}selected{% endif %}>Intermediate</option>
                            <option value="ADVANCED" {% if selected_difficulty == 'ADVANCED' %}selected{% endif %}>Advanced</option>
                        </select>
                    </div>
                    <div class="col-auto">
                        <button type="submit" class="btn btn-primary">Apply</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>

<div class="row">
    {% if challenges %}
    {% for challenge in challenges %}
    <div class="col-md-6 col-lg-4 mb-4">
        <div class="card h-100 shadow-sm border-0 hover-shadow transition-all">
            <div class="card-body">
                <div class="d-flex justify-content-between align-items-start mb-3">
                    <span class="badge 
                        {% if challenge.difficulty == 'BEGINNER' %}bg-success
                        {% elif challenge.difficulty == 'INTERMEDIATE' %}bg-warning text-dark
                        {% else %}bg-danger{% endif %}">
                        {{ challenge.difficulty|title }}
                    </span>
                    <small class="text-muted"><i class="fas fa-code me-1"></i> {{ challenge.tags }}</small>
                </div>
                <h5 class="card-title">{{ challenge.title }}</h5>
                <p class="card-text text-muted">{{ challenge.description|truncatechars:100 }}</p>
                <a href="{% url 'coding_assistant:challenge_detail' challenge.id %}" class="btn btn-outline-primary w-100 mt-3">
                    Solve Challenge <i class="fas fa-arrow-right ms-1"></i>
                </a>
            </div>
        </div>
    </div>
    {% endfor %}
    {% else %}
    <div class="col-12 text-center py-5">
        <div class="text-muted">
            <i class="fas fa-laptop-code fa-3x mb-3"></i>
            <h4>No challenges found</h4>
            <p>Try adjusting your filters or check back later!</p>
        </div>
    </div>
    {% endif %}
</div>
{% endblock %}

{% block extra_css %}
<style>
    .hover-shadow:hover {
        transform: translateY(-5px);
        box-shadow: 0 .5rem 1rem rgba(0,0,0,.15)!important;
    }
    .transition-all {
        transition: all 0.3s ease;
    }
</style>
{% endblock %}
"""

base_dir = r"c:\Users\SUSHANTH\OneDrive\Desktop\CS2\templates\coding_assistant"

with open(os.path.join(base_dir, "explore.html"), "w", encoding="utf-8") as f:
    f.write(explore_content)
    print("Updated explore.html")

with open(os.path.join(base_dir, "challenges.html"), "w", encoding="utf-8") as f:
    f.write(challenges_content)
    print("Updated challenges.html")

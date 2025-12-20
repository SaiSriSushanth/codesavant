import os

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
        <div class="card shadow-sm border-primary">
            <div class="card-header bg-primary text-white">
                <h5 class="mb-0"><i class="fas fa-robot me-2"></i>Generate Custom Challenge</h5>
            </div>
            <div class="card-body">
                <p>Can't find what you're looking for? Ask our AI to create a unique challenge for you!</p>
                <form id="generateForm" class="row g-3">
                    <div class="col-md-3">
                        <label for="gen_language" class="form-label">Language</label>
                        <select id="gen_language" class="form-select" required>
                            <option value="python">Python</option>
                            <option value="javascript">JavaScript</option>
                            <option value="java">Java</option>
                            <option value="cpp">C++</option>
                        </select>
                    </div>
                    <div class="col-md-3">
                        <label for="gen_difficulty" class="form-label">Difficulty</label>
                        <select id="gen_difficulty" class="form-select" required>
                            <option value="BEGINNER">Beginner</option>
                            <option value="INTERMEDIATE" selected>Intermediate</option>
                            <option value="ADVANCED">Advanced</option>
                        </select>
                    </div>
                    <div class="col-md-4">
                        <label for="gen_topic" class="form-label">Topic (Optional)</label>
                        <input type="text" id="gen_topic" class="form-control" placeholder="e.g. Recursion, Arrays, DP">
                    </div>
                    <div class="col-md-2 d-flex align-items-end">
                        <button type="submit" class="btn btn-primary w-100" id="generateBtn">
                            <span class="spinner-border spinner-border-sm d-none" role="status" aria-hidden="true"></span>
                            Generate
                        </button>
                    </div>
                </form>
            </div>
        </div>
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

{% block extra_js %}
<script>
document.getElementById('generateForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const btn = document.getElementById('generateBtn');
    const spinner = btn.querySelector('.spinner-border');
    const originalText = btn.childNodes[2].textContent; // "Generate" text
    
    // Disable button and show spinner
    btn.disabled = true;
    spinner.classList.remove('d-none');
    btn.childNodes[2].textContent = ' Generating...';
    
    const data = {
        language: document.getElementById('gen_language').value,
        difficulty: document.getElementById('gen_difficulty').value,
        topic: document.getElementById('gen_topic').value
    };
    
    fetch('{% url "coding_assistant:generate_challenge" %}', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token }}'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            window.location.href = `/challenges/${data.challenge_id}/`;
        } else {
            alert('Error generating challenge: ' + (data.error || 'Unknown error'));
            // Reset button
            btn.disabled = false;
            spinner.classList.add('d-none');
            btn.childNodes[2].textContent = originalText;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred. Please try again.');
        // Reset button
        btn.disabled = false;
        spinner.classList.add('d-none');
        btn.childNodes[2].textContent = originalText;
    });
});
</script>
{% endblock %}
"""

base_dir = r"c:\Users\SUSHANTH\OneDrive\Desktop\CS2\templates\coding_assistant"

with open(os.path.join(base_dir, "challenges.html"), "w", encoding="utf-8") as f:
    f.write(challenges_content)
    print("Updated challenges.html")

# CodeSavant Platform

A Django web application that uses GPT-4-Turbo to analyze coding patterns and tailor learning resources, challenges, and feedback to individual developers.

## Features

- Interactive code editor with syntax highlighting
- AI-powered code analysis using GPT-4-Turbo
- Personalized learning resources based on coding patterns
- Custom coding challenges tailored to skill level
- Code optimization and explanation
- Debugging assistance
- Save and track progress over time

## Screenshot

![CodeSavant Platform](https://placeholder-for-screenshot.png)

## Requirements

- Python 3.8+
- Django 4.2+
- OpenAI API key

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/codesavant.git
cd codesavant
```

2. Create a virtual environment and activate it:

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

3. Install the required packages:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root directory (copy from `.env.example`):

```bash
cp .env.example .env
```

5. Edit the `.env` file and add your OpenAI API key:

```
OPENAI_API_KEY=your_api_key_here
```

6. Run migrations:

```bash
python manage.py migrate
```

7. Create a superuser (admin):

```bash
python manage.py createsuperuser
```

8. Run the development server:

```bash
python manage.py runserver
```

9. Open your browser and navigate to http://127.0.0.1:8000/

## Usage

1. Log in with your superuser account
2. Navigate to the code editor
3. Write or paste your code
4. Select the programming language
5. Use the AI tools to analyze, optimize, explain, or debug your code
6. Get personalized learning resources and coding challenges
7. Save your code snippets and track your progress

## Project Structure

```
codesavant/
├── code_assistant_platform/  # Project settings
├── coding_assistant/         # Main app
│   ├── models.py             # Data models
│   ├── views.py              # Views and API endpoints
│   └── urls.py               # URL routing
├── static/                   # Static files (CSS, JS)
├── templates/                # HTML templates
├── .env.example              # Environment variables template
├── manage.py                 # Django management script
└── requirements.txt          # Python dependencies
```

## Technologies Used

- Django: Web framework
- OpenAI API: GPT-3.5-Turbo for code analysis
- CodeMirror: Code editor with syntax highlighting
- Bootstrap 5: Frontend styling
- SQLite: Database (default, can be changed)

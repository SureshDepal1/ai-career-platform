from django.db import migrations


QUESTION_BANK = {
    'Python': [
        ('Which Python collection preserves insertion order and stores key-value pairs?', ['set', 'tuple', 'dictionary', 'list'], 2, 'Dictionaries store key-value pairs and preserve insertion order in modern Python.'),
        ('What does a Python list comprehension return?', ['A list', 'A generator only', 'A dictionary always', 'A compiled module'], 0, 'List comprehensions create a new list from an iterable.'),
        ('Which keyword handles an exception in Python?', ['catch', 'except', 'error', 'handle'], 1, 'The except clause handles exceptions raised in a try block.'),
        ('What is the purpose of a virtual environment?', ['To isolate project dependencies', 'To speed up the CPU', 'To encrypt source code', 'To replace Git'], 0, 'Virtual environments isolate installed packages between projects.'),
    ],
    'SQL': [
        ('Which SQL clause filters rows before grouping?', ['HAVING', 'WHERE', 'ORDER BY', 'LIMIT'], 1, 'WHERE filters individual rows before GROUP BY is applied.'),
        ('Which operation combines rows from related tables?', ['JOIN', 'MERGE FILE', 'APPEND ONLY', 'CONNECT'], 0, 'JOIN combines rows using a relationship between tables.'),
        ('Which command changes data already stored in a table?', ['SELECT', 'UPDATE', 'DESCRIBE', 'GRANT'], 1, 'UPDATE modifies existing rows.'),
        ('What does a primary key provide?', ['A unique row identity', 'Automatic backups', 'Encryption', 'A table description'], 0, 'A primary key uniquely identifies each row.'),
    ],
    'Django': [
        ('Which Django component maps URLs to views?', ['URLconf', 'Template engine', 'Migration', 'Admin action'], 0, 'Django URLconf maps URL patterns to views.'),
        ('What does a Django migration represent?', ['A database schema change', 'A browser session', 'A CSS bundle', 'An API token'], 0, 'Migrations record and apply database schema changes.'),
        ('Which Django feature provides database access through Python objects?', ['ORM', 'WSGI only', 'Middleware cache', 'Staticfiles'], 0, 'The Django ORM maps models to database tables.'),
        ('What is a Django model?', ['A Python representation of stored data', 'A deployment server', 'A template filter', 'A CSS component'], 0, 'Models define the structure and behavior of persisted data.'),
    ],
    'Machine Learning': [
        ('What is supervised learning trained with?', ['Labeled examples', 'Only random noise', 'No data', 'HTML templates'], 0, 'Supervised learning learns from examples with known target labels.'),
        ('What is overfitting?', ['Memorizing training data and generalizing poorly', 'Using too little code', 'A database lock', 'Improving validation accuracy'], 0, 'An overfit model performs well on training data but poorly on unseen data.'),
        ('What does a validation set help estimate?', ['Generalization during model selection', 'CPU temperature', 'Database size', 'Source code length'], 0, 'Validation data helps compare models and tune hyperparameters.'),
        ('Which metric is common for binary classification?', ['Accuracy', 'File size', 'Latency only', 'Memory address'], 0, 'Accuracy is one common binary classification metric.'),
    ],
    'Git': [
        ('Which Git command creates a local copy of a remote repository?', ['git clone', 'git branch', 'git stash', 'git tag'], 0, 'git clone copies a repository and its history locally.'),
        ('What does git commit create?', ['A snapshot in repository history', 'A remote server', 'A database table', 'A deployment container'], 0, 'A commit records a snapshot of staged changes.'),
        ('Which command shows changed files?', ['git status', 'git init', 'git remote', 'git config'], 0, 'git status reports the working tree and staging area.'),
        ('What is a Git branch?', ['An independent line of development', 'A password', 'A package manager', 'A database index'], 0, 'Branches let developers work on separate lines of development.'),
    ],
    'REST APIs': [
        ('Which HTTP method is commonly used to retrieve a resource?', ['GET', 'POST', 'PATCH', 'DELETE'], 0, 'GET requests retrieve representations of resources.'),
        ('What does HTTP status 201 indicate?', ['Created', 'Unauthorized', 'Not found', 'Server error'], 0, '201 means a resource was successfully created.'),
        ('What does stateless mean for a REST API?', ['Each request contains the context needed to process it', 'The server never responds', 'Data cannot be stored', 'Only one user is supported'], 0, 'Stateless requests do not rely on stored client session context.'),
        ('Which format is commonly used for REST API payloads?', ['JSON', 'BMP', 'WAV', 'EXE'], 0, 'JSON is a common interoperable API representation format.'),
    ],
}


def seed_questions(apps, schema_editor):
    Skill = apps.get_model('careers', 'Skill')
    Question = apps.get_model('assessments', 'AssessmentQuestion')
    for skill_name, questions in QUESTION_BANK.items():
        skill = Skill.objects.filter(name__iexact=skill_name).first()
        if not skill:
            continue
        for question, options, correct_option, explanation in questions:
            Question.objects.get_or_create(
                skill=skill,
                question=question,
                defaults={
                    'options': options,
                    'correct_option': correct_option,
                    'explanation': explanation,
                },
            )


def remove_questions(apps, schema_editor):
    apps.get_model('assessments', 'AssessmentQuestion').objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ('assessments', '0001_initial'),
        ('careers', '0003_roadmap_learningresource'),
    ]

    operations = [migrations.RunPython(seed_questions, remove_questions)]

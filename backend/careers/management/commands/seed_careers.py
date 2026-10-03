from django.core.management.base import BaseCommand
from django.db import transaction

from careers.models import (
    Career,
    CareerSkill,
    LearningResource,
    Roadmap,
    Skill,
)


CATEGORIES = {
    'Software Development': (
        'Backend Developer,Frontend Developer,Full Stack Developer,Software Engineer,'
        'Web Developer,Mobile App Developer,Android Developer,iOS Developer,'
        'React Developer,Node.js Developer,Python Developer,Java Developer,.NET Developer,'
        'PHP Developer,Django Developer,Laravel Developer,Software Architect,'
        'DevOps Engineer,Site Reliability Engineer'
    ),
    'Data & AI': (
        'Data Analyst,Data Scientist,Machine Learning Engineer,AI Engineer,'
        'Deep Learning Engineer,NLP Engineer,Computer Vision Engineer,Generative AI Engineer,'
        'MLOps Engineer,Data Engineer,Data Architect,Business Intelligence Analyst,'
        'Business Intelligence Developer,Research Scientist'
    ),
    'Cybersecurity': (
        'Cybersecurity Analyst,Cybersecurity Engineer,Security Engineer,'
        'Information Security Analyst,Penetration Tester,Ethical Hacker,Security Consultant,'
        'Cloud Security Engineer,Application Security Engineer,SOC Analyst,'
        'Digital Forensics Analyst'
    ),
    'Cloud & Infrastructure': (
        'Cloud Engineer,Cloud Architect,AWS Cloud Engineer,Azure Cloud Engineer,'
        'Google Cloud Engineer,Infrastructure Engineer,Network Engineer,Systems Administrator,'
        'Linux System Administrator,Database Administrator'
    ),
    'UI/UX & Design': (
        'UI Designer,UX Designer,UI/UX Designer,Product Designer,Graphic Designer,'
        'Web Designer,Interaction Designer,UX Researcher,Motion Graphics Designer,3D Designer'
    ),
    'Business & Management': (
        'Business Analyst,Product Manager,Project Manager,Program Manager,Operations Manager,'
        'IT Manager,Technology Consultant,Management Consultant,Business Consultant,'
        'Product Owner,Scrum Master,Operations Analyst'
    ),
    'Marketing & Sales': (
        'Digital Marketing Specialist,Digital Marketing Manager,SEO Specialist,SEO Manager,'
        'Social Media Manager,Social Media Specialist,Content Marketing Specialist,'
        'Content Strategist,Email Marketing Specialist,Marketing Analyst,Brand Manager,'
        'Sales Executive,Sales Manager,Business Development Executive,'
        'Business Development Manager,Account Manager'
    ),
    'Finance & Accounting': (
        'Accountant,Financial Analyst,Financial Manager,Investment Analyst,Investment Banker,'
        'Auditor,Tax Consultant,Risk Analyst,Credit Analyst,Financial Controller,'
        'Management Accountant,Data Analyst - Finance'
    ),
    'Human Resources': (
        'HR Specialist,HR Manager,Recruitment Specialist,Talent Acquisition Specialist,'
        'Talent Manager,HR Business Partner,Learning & Development Specialist,'
        'Compensation & Benefits Analyst'
    ),
    'Engineering': (
        'Civil Engineer,Mechanical Engineer,Electrical Engineer,Electronics Engineer,'
        'Computer Engineer,Chemical Engineer,Industrial Engineer,Environmental Engineer,'
        'Biomedical Engineer,Telecommunications Engineer,Mechatronics Engineer'
    ),
    'Healthcare': (
        'Healthcare Administrator,Health Data Analyst,Health Information Manager,'
        'Medical Laboratory Technologist,Clinical Research Associate,Public Health Specialist,'
        'Healthcare IT Specialist'
    ),
    'Education': (
        'Teacher,Lecturer,Instructional Designer,Curriculum Developer,Education Consultant,'
        'E-Learning Specialist,Academic Coordinator'
    ),
    'Writing & Media': (
        'Technical Writer,Copywriter,Content Writer,Editor,Proofreader,Journalist,'
        'Script Writer,Video Editor,Video Producer,Photographer'
    ),
    'Other Professional': (
        'Virtual Assistant,Administrative Assistant,Executive Assistant,'
        'Customer Support Specialist,Customer Success Manager,Supply Chain Analyst,'
        'Supply Chain Manager,Procurement Specialist,Logistics Coordinator,'
        'Quality Assurance Engineer,QA Analyst,Test Automation Engineer,Product Analyst,'
        'Research Analyst'
    ),
}

CATEGORY_SKILLS = {
    'Software Development': [
        ('Programming', 'Programming', 4), ('Git', 'Tools', 3),
        ('REST APIs', 'Backend', 4), ('Testing', 'Engineering', 3),
        ('SQL', 'Data', 3), ('Communication', 'Professional', 2),
    ],
    'Data & AI': [
        ('Python', 'Programming', 4), ('Statistics', 'Mathematics', 4),
        ('SQL', 'Data', 3), ('Data Visualization', 'Analytics', 3),
        ('Git', 'Tools', 2), ('Communication', 'Professional', 2),
    ],
    'Cybersecurity': [
        ('Networking', 'Infrastructure', 4), ('Linux', 'Infrastructure', 3),
        ('Cybersecurity Fundamentals', 'Security', 5),
        ('Security Monitoring', 'Security', 4), ('Python', 'Programming', 2),
        ('Incident Response', 'Security', 4),
    ],
    'Cloud & Infrastructure': [
        ('Cloud Computing', 'Infrastructure', 5), ('Linux', 'Infrastructure', 4),
        ('Networking', 'Infrastructure', 4), ('Docker', 'DevOps', 3),
        ('Infrastructure as Code', 'DevOps', 3), ('Monitoring', 'Operations', 3),
    ],
    'UI/UX & Design': [
        ('User Research', 'Design', 4), ('Wireframing', 'Design', 4),
        ('Visual Design', 'Design', 4), ('Prototyping', 'Design', 3),
        ('Communication', 'Professional', 3), ('Design Tools', 'Design', 3),
    ],
    'Business & Management': [
        ('Business Analysis', 'Business', 4), ('Project Management', 'Management', 4),
        ('Communication', 'Professional', 5), ('Leadership', 'Management', 3),
        ('Data Analysis', 'Analytics', 3), ('Stakeholder Management', 'Business', 4),
    ],
    'Marketing & Sales': [
        ('Marketing Strategy', 'Marketing', 4), ('Communication', 'Professional', 5),
        ('Content Marketing', 'Marketing', 3), ('Data Analysis', 'Analytics', 3),
        ('Customer Relationship Management', 'Sales', 3), ('Copywriting', 'Writing', 3),
    ],
    'Finance & Accounting': [
        ('Accounting', 'Finance', 5), ('Financial Analysis', 'Finance', 4),
        ('Excel', 'Tools', 4), ('Statistics', 'Mathematics', 3),
        ('Data Analysis', 'Analytics', 3), ('Communication', 'Professional', 2),
    ],
    'Human Resources': [
        ('Recruitment', 'Human Resources', 4), ('Communication', 'Professional', 5),
        ('Employee Relations', 'Human Resources', 4), ('HR Information Systems', 'Human Resources', 3),
        ('Project Management', 'Management', 2), ('Leadership', 'Management', 3),
    ],
    'Engineering': [
        ('Engineering Design', 'Engineering', 5), ('Mathematics', 'Engineering', 4),
        ('Problem Solving', 'Professional', 4), ('Project Management', 'Management', 3),
        ('Computer Aided Design', 'Engineering', 3), ('Communication', 'Professional', 2),
    ],
    'Healthcare': [
        ('Healthcare Systems', 'Healthcare', 5), ('Data Analysis', 'Analytics', 3),
        ('Healthcare Regulations', 'Healthcare', 4), ('Communication', 'Professional', 4),
        ('Research Methods', 'Research', 3), ('Documentation', 'Professional', 3),
    ],
    'Education': [
        ('Teaching', 'Education', 5), ('Curriculum Design', 'Education', 4),
        ('Communication', 'Professional', 5), ('Assessment Design', 'Education', 3),
        ('Instructional Technology', 'Education', 3), ('Leadership', 'Management', 2),
    ],
    'Writing & Media': [
        ('Writing', 'Media', 5), ('Editing', 'Media', 4),
        ('Communication', 'Professional', 4), ('Storytelling', 'Media', 4),
        ('Content Strategy', 'Marketing', 3), ('Research Methods', 'Research', 2),
    ],
    'Other Professional': [
        ('Communication', 'Professional', 5), ('Customer Service', 'Professional', 4),
        ('Organization', 'Professional', 4), ('Data Analysis', 'Analytics', 2),
        ('Problem Solving', 'Professional', 3), ('Project Management', 'Management', 2),
    ],
}

TITLE_SKILLS = {
    'Backend Developer': [('Python', 'Programming', 5), ('Django', 'Backend', 5),
                          ('Database Design', 'Data', 4), ('Docker', 'DevOps', 3),
                          ('Authentication and JWT', 'Security', 4)],
    'Frontend Developer': [('HTML', 'Frontend', 5), ('CSS', 'Frontend', 5),
                           ('JavaScript', 'Programming', 5), ('React', 'Frontend', 4),
                           ('Responsive Design', 'Design', 4)],
    'Full Stack Developer': [('JavaScript', 'Programming', 5), ('React', 'Frontend', 4),
                             ('Node.js', 'Backend', 4), ('SQL', 'Data', 4),
                             ('Docker', 'DevOps', 3)],
    'Machine Learning Engineer': [('Python', 'Programming', 5), ('Machine Learning', 'AI', 5),
                                  ('Statistics', 'Mathematics', 4), ('NumPy', 'AI', 3),
                                  ('Pandas', 'AI', 3), ('Deep Learning', 'AI', 4)],
    'Data Analyst': [('SQL', 'Data', 5), ('Excel', 'Tools', 4), ('Python', 'Programming', 3),
                     ('Pandas', 'AI', 3), ('Data Cleaning', 'Analytics', 4),
                     ('Power BI and Tableau', 'Analytics', 4)],
    'Data Scientist': [('Python', 'Programming', 5), ('Machine Learning', 'AI', 4),
                       ('Statistics', 'Mathematics', 5), ('Pandas', 'AI', 4),
                       ('Data Visualization', 'Analytics', 4)],
    'Cybersecurity Analyst': [('Networking', 'Infrastructure', 5), ('Linux', 'Infrastructure', 4),
                              ('SIEM', 'Security', 5), ('Threat Detection', 'Security', 5),
                              ('Incident Response', 'Security', 4), ('Security Tools', 'Security', 3)],
    'Cloud Engineer': [('Cloud Computing', 'Infrastructure', 5), ('AWS', 'Cloud', 4),
                       ('Docker', 'DevOps', 4), ('Kubernetes', 'DevOps', 4),
                       ('Infrastructure as Code', 'DevOps', 4)],
    'DevOps Engineer': [('Linux', 'Infrastructure', 4), ('Docker', 'DevOps', 5),
                        ('Kubernetes', 'DevOps', 4), ('CI/CD', 'DevOps', 5),
                        ('Cloud Computing', 'Infrastructure', 4)],
    'Product Manager': [('Product Strategy', 'Business', 5), ('User Research', 'Product', 4),
                        ('Roadmapping', 'Product', 4), ('Communication', 'Professional', 5),
                        ('Data Analysis', 'Analytics', 3)],
}

RESOURCE_CATALOG = {
    'Python': ('Python Documentation', 'Learn the Python language and standard library.', 'Documentation', 'https://docs.python.org/3/', 'Build a small command-line tool.', 'Write readable Python programs.'),
    'Django': ('Django Documentation', 'Learn how to build secure web applications with Django.', 'Documentation', 'https://docs.djangoproject.com/en/stable/', 'Build a CRUD web application.', 'Create maintainable Django applications.'),
    'REST APIs': ('Django REST framework Tutorial', 'Learn how to build browsable, production-ready REST APIs.', 'Tutorial', 'https://www.django-rest-framework.org/tutorial/quickstart/', 'Build an authenticated JSON API.', 'Design and test REST endpoints.'),
    'Docker': ('Docker Get Started', 'Learn containerization and essential Docker workflows.', 'Documentation', 'https://docs.docker.com/get-started/', 'Containerize a web application.', 'Package and run services consistently.'),
    'Git': ('Git Documentation', 'Learn version control workflows for collaborative development.', 'Documentation', 'https://git-scm.com/doc', 'Publish a project with a clean commit history.', 'Collaborate safely with Git.'),
    'SQL': ('PostgreSQL Documentation', 'Practice relational queries and database fundamentals.', 'Documentation', 'https://www.postgresql.org/docs/', 'Design and query a relational database.', 'Write reliable SQL queries.'),
    'Database Design': ('PostgreSQL Documentation', 'Learn relational modeling, constraints, and query planning.', 'Documentation', 'https://www.postgresql.org/docs/', 'Model a database for a real application.', 'Design normalized relational schemas.'),
    'Authentication and JWT': ('Django REST framework Authentication', 'Learn authentication and permission patterns for APIs.', 'Documentation', 'https://www.django-rest-framework.org/api-guide/authentication/', 'Add JWT authentication to an API.', 'Secure API access with clear permissions.'),
    'JavaScript': ('MDN JavaScript Guide', 'Learn the core language and browser APIs.', 'Guide', 'https://developer.mozilla.org/en-US/docs/Web/JavaScript', 'Build an interactive browser application.', 'Write robust modern JavaScript.'),
    'React': ('React Learn', 'Learn React fundamentals by building user interfaces.', 'Tutorial', 'https://react.dev/learn', 'Build a dashboard with reusable components.', 'Compose responsive React interfaces.'),
    'Statistics': ('OpenStax Introductory Statistics', 'Build a practical foundation in descriptive and inferential statistics.', 'Course', 'https://openstax.org/details/books/introductory-statistics-2e', 'Analyze a real-world dataset.', 'Interpret uncertainty and statistical results.'),
    'NumPy': ('NumPy User Guide', 'Learn numerical arrays and scientific computing workflows.', 'Documentation', 'https://numpy.org/doc/', 'Implement a numerical data transformation.', 'Work efficiently with numerical data.'),
    'Pandas': ('pandas Documentation', 'Learn data loading, cleaning, and analysis with pandas.', 'Documentation', 'https://pandas.pydata.org/docs/', 'Clean and analyze a public dataset.', 'Prepare reproducible tabular analyses.'),
    'Machine Learning': ('scikit-learn User Guide', 'Learn core machine-learning workflows and model evaluation.', 'Guide', 'https://scikit-learn.org/stable/user_guide.html', 'Train and evaluate a supervised model.', 'Build an evaluated ML pipeline.'),
    'Deep Learning': ('PyTorch Tutorials', 'Learn the fundamentals of deep learning with PyTorch.', 'Tutorial', 'https://pytorch.org/tutorials/', 'Train a small image classifier.', 'Build and evaluate neural networks.'),
    'Data Visualization': ('Matplotlib Documentation', 'Learn to communicate data with clear visualizations.', 'Documentation', 'https://matplotlib.org/stable/contents.html', 'Create a data story with charts.', 'Choose and explain effective visualizations.'),
    'Data Cleaning': ('pandas User Guide', 'Practice handling missing, inconsistent, and duplicated data.', 'Guide', 'https://pandas.pydata.org/docs/user_guide/index.html', 'Create a reusable cleaning notebook.', 'Produce analysis-ready datasets.'),
    'Power BI and Tableau': ('Microsoft Power BI Learning', 'Learn dashboarding and business intelligence fundamentals.', 'Course', 'https://learn.microsoft.com/en-us/training/powerplatform/power-bi/', 'Build an interactive KPI dashboard.', 'Deliver a clear stakeholder dashboard.'),
    'Networking': ('Cisco Networking Basics', 'Build practical foundations in networking concepts and protocols.', 'Course', 'https://www.cisco.com/c/en/us/training-events/training-certifications/training/training-services/courses/networking-basics.html', 'Document and troubleshoot a small network.', 'Explain common network behavior.'),
    'Linux': ('Linux Documentation', 'Learn essential Linux administration and command-line skills.', 'Documentation', 'https://www.kernel.org/doc/html/latest/', 'Automate a routine server task.', 'Navigate and manage Linux systems.'),
    'SIEM': ('Microsoft Sentinel Documentation', 'Learn the principles of security information and event management.', 'Documentation', 'https://learn.microsoft.com/en-us/azure/sentinel/', 'Create detections from sample logs.', 'Investigate security events systematically.'),
    'Threat Detection': ('MITRE ATT&CK', 'Learn a shared knowledge base for adversary tactics and techniques.', 'Reference', 'https://attack.mitre.org/', 'Map a detection plan to ATT&CK techniques.', 'Recognize and explain common threats.'),
    'Incident Response': ('NIST Incident Response Guide', 'Learn a repeatable process for preparing for and handling incidents.', 'Guide', 'https://csrc.nist.gov/pubs/sp/800/61/r2/final', 'Write an incident response playbook.', 'Respond consistently to security incidents.'),
    'Security Tools': ('OWASP Web Security Testing Guide', 'Learn established approaches to testing application security.', 'Guide', 'https://owasp.org/www-project-web-security-testing-guide/', 'Perform a safe test against a local app.', 'Use security tools responsibly.'),
}


def canonical(value):
    return ' '.join(value.casefold().strip().split())


class Command(BaseCommand):
    help = 'Create or update the reusable career and skill catalog.'

    @transaction.atomic
    def handle(self, *args, **options):
        existing_skills = {
            canonical(skill.name): skill
            for skill in Skill.objects.all()
        }
        created_careers = 0
        created_skills = 0
        created_links = 0
        created_roadmaps = 0
        created_resources = 0

        for category, titles in CATEGORIES.items():
            base_skills = CATEGORY_SKILLS[category]
            for title in titles.split(','):
                skills = list(base_skills)
                skills.extend(TITLE_SKILLS.get(title, []))
                career, created = Career.objects.update_or_create(
                    title=title,
                    defaults={
                        'category': category,
                        'description': (
                            f'{title} roles combine {category.lower()} expertise '
                            'with practical problem solving and continuous learning.'
                        ),
                    },
                )
                created_careers += int(created)
                for name, skill_category, importance in skills:
                    key = canonical(name)
                    skill = existing_skills.get(key)
                    if skill is None:
                        skill = Skill.objects.create(
                            name=name,
                            category=skill_category,
                        )
                        existing_skills[key] = skill
                        created_skills += 1
                    else:
                        changed = False
                        if not skill.category:
                            skill.category = skill_category
                            changed = True
                        if changed:
                            skill.save(update_fields=['category'])
                    _, created = CareerSkill.objects.update_or_create(
                        career=career,
                        skill=skill,
                        defaults={'importance': importance},
                    )
                    created_links += int(created)

                roadmap, roadmap_created = Roadmap.objects.get_or_create(
                    career=career,
                    defaults={
                        'title': f'{title} Learning Roadmap',
                        'description': f'A practical learning path for {title}, ordered by the skills required for this career.',
                    },
                )
                created_roadmaps += int(roadmap_created)
                for phase, (name, skill_category, importance) in enumerate(skills, start=1):
                    skill = existing_skills[canonical(name)]
                    catalog = RESOURCE_CATALOG.get(name)
                    if not catalog:
                        continue
                    resource_title, description, resource_type, url, project, outcome = catalog
                    _, resource_created = LearningResource.objects.update_or_create(
                        roadmap=roadmap,
                        skill=skill,
                        defaults={
                            'title': resource_title,
                            'description': description,
                            'resource_type': resource_type,
                            'url': url,
                            'learning_objectives': description,
                            'practice_project': project,
                            'expected_outcome': outcome,
                            'phase': phase,
                        },
                    )
                    created_resources += int(resource_created)

        self.stdout.write(self.style.SUCCESS(
            f'Catalog ready: {Career.objects.count()} careers, '
            f'{Skill.objects.count()} skills, {created_links} relationships '
            f'({created_careers} careers and {created_skills} skills created, '
            f'{created_roadmaps} roadmaps and {created_resources} resources created).'
        ))

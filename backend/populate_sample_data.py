#!/usr/bin/env python3
"""
Script to populate the database with sample job data
"""

import os
import sys
import django
from datetime import datetime, timedelta
from decimal import Decimal

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.working_settings')
django.setup()

from api.models import (
    Company, JobCategory, JobSkill, Job, JobSkillRequirement,
    JobApplication, SavedJob, JobRecommendation, FirebaseUser
)

def create_sample_companies():
    """Create sample companies"""
    companies_data = [
        {
            'name': 'TechCorp Solutions',
            'description': 'Leading technology company specializing in AI and machine learning solutions.',
            'website': 'https://techcorp.com',
            'industry': 'Technology',
            'size': '500-1000 employees',
            'location': 'San Francisco, CA',
            'logo_url': 'https://techcorp.com/logo.png'
        },
        {
            'name': 'DataFlow Inc',
            'description': 'Data analytics and business intelligence company.',
            'website': 'https://dataflow.com',
            'industry': 'Data Analytics',
            'size': '100-500 employees',
            'location': 'New York, NY',
            'logo_url': 'https://dataflow.com/logo.png'
        },
        {
            'name': 'CloudTech Systems',
            'description': 'Cloud infrastructure and DevOps solutions provider.',
            'website': 'https://cloudtech.com',
            'industry': 'Cloud Computing',
            'size': '50-100 employees',
            'location': 'Austin, TX',
            'logo_url': 'https://cloudtech.com/logo.png'
        },
        {
            'name': 'StartupXYZ',
            'description': 'Innovative startup focused on mobile applications and user experience.',
            'website': 'https://startupxyz.com',
            'industry': 'Mobile Technology',
            'size': '10-50 employees',
            'location': 'Seattle, WA',
            'logo_url': 'https://startupxyz.com/logo.png'
        },
        {
            'name': 'FinTech Innovations',
            'description': 'Financial technology company revolutionizing digital banking.',
            'website': 'https://fintech-innovations.com',
            'industry': 'Financial Technology',
            'size': '200-500 employees',
            'location': 'Boston, MA',
            'logo_url': 'https://fintech-innovations.com/logo.png'
        }
    ]
    
    companies = []
    for data in companies_data:
        company, created = Company.objects.get_or_create(
            name=data['name'],
            defaults=data
        )
        companies.append(company)
        if created:
            print(f"✅ Created company: {company.name}")
        else:
            print(f"ℹ️  Company already exists: {company.name}")
    
    return companies

def create_sample_categories():
    """Create sample job categories"""
    categories_data = [
        {'name': 'Software Engineering', 'description': 'Software development and engineering roles'},
        {'name': 'Data Science', 'description': 'Data analysis, machine learning, and AI roles'},
        {'name': 'DevOps', 'description': 'DevOps, infrastructure, and cloud engineering roles'},
        {'name': 'Product Management', 'description': 'Product strategy and management roles'},
        {'name': 'Design', 'description': 'UI/UX design and user experience roles'},
        {'name': 'Marketing', 'description': 'Digital marketing and growth roles'},
        {'name': 'Sales', 'description': 'Sales and business development roles'},
    ]
    
    categories = []
    for data in categories_data:
        category, created = JobCategory.objects.get_or_create(
            name=data['name'],
            defaults=data
        )
        categories.append(category)
        if created:
            print(f"✅ Created category: {category.name}")
        else:
            print(f"ℹ️  Category already exists: {category.name}")
    
    return categories

def create_sample_skills():
    """Create sample job skills"""
    skills_data = [
        # Programming Languages
        {'name': 'Python', 'category': 'programming'},
        {'name': 'JavaScript', 'category': 'programming'},
        {'name': 'Java', 'category': 'programming'},
        {'name': 'React', 'category': 'programming'},
        {'name': 'Node.js', 'category': 'programming'},
        {'name': 'Django', 'category': 'programming'},
        {'name': 'Flask', 'category': 'programming'},
        {'name': 'SQL', 'category': 'programming'},
        {'name': 'TypeScript', 'category': 'programming'},
        {'name': 'Go', 'category': 'programming'},
        
        # Cloud & DevOps
        {'name': 'AWS', 'category': 'cloud'},
        {'name': 'Docker', 'category': 'cloud'},
        {'name': 'Kubernetes', 'category': 'cloud'},
        {'name': 'Azure', 'category': 'cloud'},
        {'name': 'Terraform', 'category': 'cloud'},
        
        # Data & Analytics
        {'name': 'Machine Learning', 'category': 'data'},
        {'name': 'TensorFlow', 'category': 'data'},
        {'name': 'Pandas', 'category': 'data'},
        {'name': 'NumPy', 'category': 'data'},
        {'name': 'Tableau', 'category': 'data'},
        
        # Design & UX
        {'name': 'Figma', 'category': 'design'},
        {'name': 'Adobe Creative Suite', 'category': 'design'},
        {'name': 'User Research', 'category': 'design'},
        {'name': 'Prototyping', 'category': 'design'},
        
        # Management & Soft Skills
        {'name': 'Project Management', 'category': 'management'},
        {'name': 'Agile', 'category': 'management'},
        {'name': 'Leadership', 'category': 'management'},
        {'name': 'Communication', 'category': 'soft_skills'},
    ]
    
    skills = []
    for data in skills_data:
        skill, created = JobSkill.objects.get_or_create(
            name=data['name'],
            defaults=data
        )
        skills.append(skill)
        if created:
            print(f"✅ Created skill: {skill.name}")
        else:
            print(f"ℹ️  Skill already exists: {skill.name}")
    
    return skills

def create_sample_jobs(companies, categories, skills):
    """Create sample jobs"""
    jobs_data = [
        {
            'title': 'Senior Software Engineer',
            'company': companies[0],  # TechCorp Solutions
            'category': categories[0],  # Software Engineering
            'description': 'We are looking for a senior software engineer to join our growing team. You will be responsible for designing and implementing scalable software solutions.',
            'requirements': '5+ years of experience in software development, strong knowledge of Python and Django, experience with cloud platforms.',
            'responsibilities': 'Design and develop software applications, collaborate with cross-functional teams, mentor junior developers.',
            'benefits': 'Competitive salary, health insurance, 401k, flexible work hours, remote work options.',
            'location': 'San Francisco, CA',
            'job_type': 'full-time',
            'work_location': 'hybrid',
            'salary_min': Decimal('120000.00'),
            'salary_max': Decimal('160000.00'),
            'salary_currency': 'USD',
            'salary_period': 'yearly',
            'application_deadline': datetime.now() + timedelta(days=30),
            'is_featured': True,
            'required_skills': ['Python', 'Django', 'AWS', 'Docker']
        },
        {
            'title': 'Data Scientist',
            'company': companies[1],  # DataFlow Inc
            'category': categories[1],  # Data Science
            'description': 'Join our data science team to build machine learning models and extract insights from large datasets.',
            'requirements': 'PhD or Master\'s in Data Science, 3+ years experience with ML algorithms, proficiency in Python and SQL.',
            'responsibilities': 'Develop ML models, analyze data patterns, create data visualizations, collaborate with product teams.',
            'benefits': 'Competitive salary, stock options, professional development budget, flexible schedule.',
            'location': 'New York, NY',
            'job_type': 'full-time',
            'work_location': 'remote',
            'salary_min': Decimal('100000.00'),
            'salary_max': Decimal('140000.00'),
            'salary_currency': 'USD',
            'salary_period': 'yearly',
            'application_deadline': datetime.now() + timedelta(days=45),
            'is_featured': True,
            'required_skills': ['Python', 'Machine Learning', 'TensorFlow', 'Pandas']
        },
        {
            'title': 'DevOps Engineer',
            'company': companies[2],  # CloudTech Systems
            'category': categories[2],  # DevOps
            'description': 'We need a DevOps engineer to help us scale our cloud infrastructure and improve our deployment processes.',
            'requirements': '3+ years DevOps experience, strong knowledge of AWS, Docker, and Kubernetes, experience with CI/CD.',
            'responsibilities': 'Manage cloud infrastructure, automate deployment processes, monitor system performance, ensure security.',
            'benefits': 'Competitive salary, health insurance, unlimited PTO, home office stipend.',
            'location': 'Austin, TX',
            'job_type': 'full-time',
            'work_location': 'hybrid',
            'salary_min': Decimal('90000.00'),
            'salary_max': Decimal('130000.00'),
            'salary_currency': 'USD',
            'salary_period': 'yearly',
            'application_deadline': datetime.now() + timedelta(days=20),
            'required_skills': ['AWS', 'Docker', 'Kubernetes', 'Terraform']
        },
        {
            'title': 'Full Stack Developer',
            'company': companies[3],  # StartupXYZ
            'category': categories[0],  # Software Engineering
            'description': 'Join our fast-growing startup as a full stack developer. You\'ll work on both frontend and backend development.',
            'requirements': '2+ years full stack development, proficiency in JavaScript, React, Node.js, and databases.',
            'responsibilities': 'Develop web applications, build APIs, work on frontend components, collaborate with design team.',
            'benefits': 'Competitive salary, equity, flexible hours, learning budget, team events.',
            'location': 'Seattle, WA',
            'job_type': 'full-time',
            'work_location': 'on-site',
            'salary_min': Decimal('80000.00'),
            'salary_max': Decimal('120000.00'),
            'salary_currency': 'USD',
            'salary_period': 'yearly',
            'application_deadline': datetime.now() + timedelta(days=15),
            'required_skills': ['JavaScript', 'React', 'Node.js', 'SQL']
        },
        {
            'title': 'Product Manager',
            'company': companies[4],  # FinTech Innovations
            'category': categories[3],  # Product Management
            'description': 'Lead product development for our innovative fintech solutions. Work with engineering and design teams.',
            'requirements': '3+ years product management experience, fintech background preferred, strong analytical skills.',
            'responsibilities': 'Define product roadmap, work with stakeholders, analyze user feedback, manage product launches.',
            'benefits': 'Competitive salary, bonus, health insurance, 401k, professional development.',
            'location': 'Boston, MA',
            'job_type': 'full-time',
            'work_location': 'hybrid',
            'salary_min': Decimal('110000.00'),
            'salary_max': Decimal('150000.00'),
            'salary_currency': 'USD',
            'salary_period': 'yearly',
            'application_deadline': datetime.now() + timedelta(days=25),
            'required_skills': ['Project Management', 'Agile', 'Communication', 'Leadership']
        }
    ]
    
    jobs = []
    for data in jobs_data:
        # Extract required skills
        required_skills = data.pop('required_skills', [])
        
        job, created = Job.objects.get_or_create(
            title=data['title'],
            company=data['company'],
            defaults=data
        )
        
        if created:
            print(f"✅ Created job: {job.title}")
            
            # Add skill requirements
            for skill_name in required_skills:
                try:
                    skill = JobSkill.objects.get(name=skill_name)
                    JobSkillRequirement.objects.create(
                        job=job,
                        skill=skill,
                        is_required=True,
                        experience_level='intermediate'
                    )
                except JobSkill.DoesNotExist:
                    print(f"⚠️  Skill not found: {skill_name}")
        else:
            print(f"ℹ️  Job already exists: {job.title}")
        
        jobs.append(job)
    
    return jobs

def main():
    """Main function to populate sample data"""
    print("🌱 Populating database with sample data...")
    print("=" * 50)
    
    try:
        # Create sample data
        companies = create_sample_companies()
        categories = create_sample_categories()
        skills = create_sample_skills()
        jobs = create_sample_jobs(companies, categories, skills)
        
        print("\n" + "=" * 50)
        print("🎉 Sample data population completed!")
        print(f"   Companies: {len(companies)}")
        print(f"   Categories: {len(categories)}")
        print(f"   Skills: {len(skills)}")
        print(f"   Jobs: {len(jobs)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error populating sample data: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

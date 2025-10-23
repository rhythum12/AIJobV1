from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class FirebaseUserManager(BaseUserManager):
    def create_user(self, uid, email=None):
        if not uid:
            raise ValueError("Users must have a Firebase UID")
        user = self.model(uid=uid, email=email)
        user.save(using=self._db)
        return user

class FirebaseUser(AbstractBaseUser):
    uid = models.CharField(max_length=128, unique=True)  # From Firebase
    email = models.EmailField(max_length=255, blank=True, null=True)
    display_name = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = FirebaseUserManager()

    USERNAME_FIELD = 'uid'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email or self.uid

    @property
    def is_staff(self):
        return self.is_admin

# Job-related models
class Company(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    industry = models.CharField(max_length=100, blank=True, null=True)
    size = models.CharField(max_length=50, blank=True, null=True)  # e.g., "100-500 employees"
    location = models.CharField(max_length=255, blank=True, null=True)
    logo_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Companies"

class JobCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Job Categories"

class Job(models.Model):
    JOB_TYPE_CHOICES = [
        ('full-time', 'Full-time'),
        ('part-time', 'Part-time'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
        ('freelance', 'Freelance'),
    ]

    WORK_LOCATION_CHOICES = [
        ('remote', 'Remote'),
        ('on-site', 'On-site'),
        ('hybrid', 'Hybrid'),
    ]

    # Basic job information
    title = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='jobs')
    category = models.ForeignKey(JobCategory, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Job details
    description = models.TextField()
    requirements = models.TextField()
    responsibilities = models.TextField(blank=True, null=True)
    benefits = models.TextField(blank=True, null=True)
    
    # Location and type
    location = models.CharField(max_length=255)
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, default='full-time')
    work_location = models.CharField(max_length=20, choices=WORK_LOCATION_CHOICES, default='on-site')
    
    # Salary information
    salary_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salary_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salary_currency = models.CharField(max_length=3, default='USD')
    salary_period = models.CharField(max_length=20, default='yearly')  # yearly, monthly, hourly
    
    # Application details
    application_deadline = models.DateTimeField(null=True, blank=True)
    application_url = models.URLField(blank=True, null=True)
    application_email = models.EmailField(blank=True, null=True)
    
    # Status and metadata
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    views_count = models.PositiveIntegerField(default=0)
    applications_count = models.PositiveIntegerField(default=0)
    
    # Timestamps
    posted_date = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} at {self.company.name}"

    class Meta:
        ordering = ['-posted_date', '-created_at']

class JobSkill(models.Model):
    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=50, blank=True, null=True)  # e.g., 'programming', 'design', 'management'
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class JobSkillRequirement(models.Model):
    EXPERIENCE_LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('expert', 'Expert'),
    ]

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='skill_requirements')
    skill = models.ForeignKey(JobSkill, on_delete=models.CASCADE)
    is_required = models.BooleanField(default=True)
    experience_level = models.CharField(max_length=20, choices=EXPERIENCE_LEVEL_CHOICES, default='intermediate')
    years_experience = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.job.title} - {self.skill.name}"

    class Meta:
        unique_together = ['job', 'skill']

class JobApplication(models.Model):
    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('interview_scheduled', 'Interview Scheduled'),
        ('interviewed', 'Interviewed'),
        ('rejected', 'Rejected'),
        ('accepted', 'Accepted'),
        ('withdrawn', 'Withdrawn'),
    ]

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    user = models.ForeignKey(FirebaseUser, on_delete=models.CASCADE, related_name='applications')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')
    
    # Application details
    cover_letter = models.TextField(blank=True, null=True)
    resume_url = models.URLField(blank=True, null=True)
    portfolio_url = models.URLField(blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    
    # Additional information
    expected_salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    availability_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True, null=True)
    
    # Timestamps
    applied_date = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} applied for {self.job.title}"

    class Meta:
        unique_together = ['job', 'user']
        ordering = ['-applied_date']

class SavedJob(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='saved_by')
    user = models.ForeignKey(FirebaseUser, on_delete=models.CASCADE, related_name='saved_jobs')
    saved_date = models.DateTimeField(default=timezone.now)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.email} saved {self.job.title}"

    class Meta:
        unique_together = ['job', 'user']
        ordering = ['-saved_date']

class JobRecommendation(models.Model):
    user = models.ForeignKey(FirebaseUser, on_delete=models.CASCADE, related_name='job_recommendations')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='recommendations')
    match_score = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(100.0)])
    reason = models.TextField(blank=True, null=True)
    algorithm_version = models.CharField(max_length=50, default='v1.0')
    created_at = models.DateTimeField(auto_now_add=True)
    is_viewed = models.BooleanField(default=False)
    is_applied = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.email} - {self.job.title} ({self.match_score}%)"

    class Meta:
        unique_together = ['user', 'job']
        ordering = ['-match_score', '-created_at']

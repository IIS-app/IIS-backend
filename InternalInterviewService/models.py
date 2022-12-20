from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.db.models.fields import DateTimeField, DateField

# Create your models here.

# Create custom user manager here
class UserManager(BaseUserManager):
  def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
    if not email:
        raise ValueError('Users must have an email address')
    if not password:
        raise ValueError('Please provide a password')
    now = timezone.now()
    email = self.normalize_email(email)
    user = self.model(
        email=email,
        is_staff=is_staff, 
        is_active=True,
        is_superuser=is_superuser, 
        last_login=now,
        date_joined=now, 
        **extra_fields
    )
    user.set_password(password)
    user.save(using=self._db)
    return user

  def create_user(self, email, password, **extra_fields):
    return self._create_user(email, password, False, False, **extra_fields)

  def create_superuser(self, email, password, **extra_fields):
    user=self._create_user(email, password, True, True, **extra_fields)
    return user

# Create User model here
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=254, unique=True)
    first_name = models.CharField(max_length=254)
    last_name = models.CharField(max_length=254)
    id = models.BigAutoField(primary_key=True, unique=True, editable=False)
    codename = models.CharField(max_length=20)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    linkedin = models.URLField(null=True, blank=True)
    github = models.URLField(null=True, blank=True)
    codepen = models.URLField(null=True, blank=True)
    portfolio = models.URLField(null=True, blank=True)
    personal_pitch = models.TextField(null=True, blank=True, max_length=1000)


    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'codename']

    objects = UserManager()

    def get_absolute_url(self):
        return "/users/%i/" % (self.pk)

    # personal_pitch
    # links

# Create Question model here
class Question(models.Model):
  INTERVIEW_QUESTIONS = 'IQ'
  COMPANY_QUESTIONS = 'CQ'
  QUESTION_TYPE = [
      (INTERVIEW_QUESTIONS, 'Interview Questions'),
      (COMPANY_QUESTIONS, 'Company Questions'),
  ]
  question_type = models.CharField(
      max_length=2,
      choices=QUESTION_TYPE)
  question = models.CharField(max_length=50)
  created_date = models.DateField(auto_now_add=True)
  answer = models.TextField(null=True)
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions')
  
# Create StarrQuestions model here
class StarrQuestions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.TextField(max_length=500)
    summary = models.TextField(max_length=1000, null=True, blank=True)
    situation = models.TextField(max_length=500, null=True, blank=True)
    task = models.TextField(max_length=500, null=True, blank=True)
    action = models.TextField(max_length=500, null=True, blank=True)
    reflection = models.TextField(max_length=500, null=True, blank=True)
    result = models.TextField(max_length=500, null=True, blank=True)

# Create Win model here
class Win(models.Model):
  title = models.CharField(max_length=50)
  created_date = models.DateTimeField(auto_now_add=True)
  occured_date = models.DateField(null=True, blank=True, auto_now_add=False)
  win = models.TextField()
  win_picture = models.ImageField(null=True, blank=True)
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wins')
   
  def __str__(self):
        return self.title

# Create TargetCompany model here
class TargetCompany(models.Model):
    RANK_CHOICES=[
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=155)
    rank = models.CharField(choices=RANK_CHOICES, null=True, blank=True,max_length=10)
    website = models.URLField()
    job_page = models.URLField(null =True, blank=True)
    comments = models.TextField(max_length=5000, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# Create CompanyContacts model here
class CompanyContacts(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)
    notes = models.TextField(max_length=5000, null=True, blank=True)
    company = models.ForeignKey(TargetCompany, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

# Create Job model here
class Job(models.Model):
  title = models.CharField(max_length=50)
  notes = models.TextField()
  job_listing = models.URLField()
  company = models.ForeignKey(TargetCompany, on_delete=models.CASCADE, related_name='jobs')
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='jobs')

# Create Resume model here
class Resume(models.Model):
    title = models.CharField(max_length=50, null=True, blank=True)
    notes = models.TextField(max_length=5000, null=True, blank=True)
    file = models.FileField(upload_to='resume')
    job = models.ForeignKey(Job, null=True, on_delete=models.CASCADE, related_name='resumes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resumes')

# Create CoverLetter model here
class CoverLetter(models.Model):
    title = models.CharField(max_length=50)
    notes = models.TextField(max_length=5000, null=True, blank=True)
    file = models.FileField(upload_to='coverletter')
    job = models.ForeignKey(Job, null=True, on_delete=models.CASCADE, related_name='cover_letters')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cover_letters')
    
#Create Dossier model here
class Dossier(models.Model):
  title = models.CharField(max_length=50)
  job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='dossiers')
  resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='dossiers')
  cover_letter = models.ForeignKey(CoverLetter, on_delete=models.CASCADE, related_name='dossiers')
  starrs = models.ManyToManyField(StarrQuestions)
  questions = models.ManyToManyField(Question)
  wins = models.ManyToManyField(Win)
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dossiers')

# Create Interview model here
class Interview(models.Model):
  title = models.CharField(max_length=50)
  job = models.ForeignKey(Job, null=True, on_delete=models.CASCADE, related_name='jobs')
  notes = models.TextField()
  date = models.DateField(null=True, blank=True, auto_now_add=False)
  time = models.TimeField(null=True, blank=True, auto_now_add=False)
  thank_you_letter = models.TextField()
  thank_you_letter_file = models.FileField(upload_to='thank_you_letter')
  questions_asked = models.TextField()
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='interviews')

# Create Goal model here
class Goal(models.Model):
  title = models.CharField(max_length=50)
  number = models.PositiveIntegerField()
  metric = models.CharField(max_length=50)
  created_date = models.DateField(auto_now_add=True)
  date_to_complete = models.DateField(blank=True, null=True, auto_now_add=False)
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='goals')

class ShortPersonalPitch(models.Model):
    title = models.CharField(max_length=50)
    user =  models.ForeignKey(User, on_delete=models.CASCADE, related_name='short_personal_pitch')
    pitch = models.TextField(max_length=650)

class LongPersonalPitch(models.Model):
    title = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='long_personal_pitch')
    pitch = models.TextField(max_length=1300)

class Links(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='links')
    title = models.CharField(max_length=20)
    link = models.URLField()

class CompanyComments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='company_comments')
    company = models.ForeignKey(TargetCompany, on_delete=models.CASCADE, related_name='company_comments')
    contact = models.ForeignKey(CompanyContacts, on_delete=models.CASCADE, related_name='comment_contact', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    important_date = models.DateTimeField(blank=True, null=True)
    notes = models.TextField()

class JobComments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="job_comments")
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='job_comments')
    created_at = models.DateTimeField(auto_now_add=True),
    updated_at = models.DateTimeField(auto_now= True)
    important_date = models.DateTimeField(blank=True,null=True)
    notes = models.TextField()
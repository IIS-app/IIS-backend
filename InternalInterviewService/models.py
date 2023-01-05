from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.db.models.fields import DateTimeField, DateField
from taggit.managers import TaggableManager


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
      (COMPANY_QUESTIONS, 'Company Questions')
  ]
  question_type = models.CharField(max_length=2,choices=QUESTION_TYPE)
  question = models.CharField(max_length=75)
  answer = models.TextField(null=True, blank=True)
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions')
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now= True)
  draft = models.BooleanField(default=True)
  
  tags = TaggableManager(blank=True)

  def __str__(self):
    return self.question

class SystemQuestion(models.Model):
  INTERVIEW_QUESTIONS = 'IQ'
  COMPANY_QUESTIONS = 'CQ'
  QUESTION_TYPE = [
      (INTERVIEW_QUESTIONS, 'Interview Questions'),
      (COMPANY_QUESTIONS, 'Company Questions')
  ]
  question_type = models.CharField(max_length=2,choices=QUESTION_TYPE)
  question = models.CharField(max_length=75)
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='system_questions')
  
  tags = TaggableManager(blank=True)

  def __str__(self):
    return self.question

  
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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now= True)
    draft = models.BooleanField(default=True)

    tags = TaggableManager(blank=True)

    def __str__(self):
        return self.question

# Create Win model here
class Win(models.Model):
  title = models.CharField(max_length=75)
  occured_date = models.DateField(null=True, blank=True, auto_now_add=False)
  win = models.TextField()
  win_picture = models.ImageField(upload_to='win_picture', null=True, blank=True)
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wins')
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now= True)
  draft = models.BooleanField(default=True)

  tags = TaggableManager(blank=True)
   
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
    website = models.URLField(null=True, blank=True)
    job_page = models.URLField(null =True, blank=True)
    comments = models.TextField(max_length=5000, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now= True)

    tags = TaggableManager(blank=True)

    def __str__(self):
        return self.company_name

# Create CompanyContacts model here
class CompanyContacts(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)
    notes = models.TextField(max_length=5000, null=True, blank=True)
    company = models.ForeignKey(TargetCompany, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now= True)

    def __str__(self):
        return self.name

# Create Job model here
class Job(models.Model):
  title = models.CharField(max_length=75)
  notes = models.TextField(null=True, blank=True)
  job_listing = models.URLField()
  Dossier = models.TextField(null=True, blank=True)
  company = models.ForeignKey(TargetCompany, on_delete=models.CASCADE, related_name='jobs', null=True, blank=True)
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='jobs')
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now= True)

  tags = TaggableManager(blank=False)

  def __str__(self):
    return self.title

# Create Resume model here
class Resume(models.Model):
    title = models.CharField(max_length=75)
    notes = models.TextField(max_length=5000, null=True, blank=True)
    file = models.FileField(upload_to='resume', null=True, blank=True)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='resumes', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resumes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now= True)

    tags = TaggableManager(blank=True)

    def __str__(self):
        return self.title

# Create CoverLetter model here
class CoverLetter(models.Model):
    title = models.CharField(max_length=75)
    notes = models.TextField(max_length=5000, null=True, blank=True)
    file = models.FileField(upload_to='coverletter',null=True, blank=True)
    job = models.ForeignKey(Job, null=True, on_delete=models.CASCADE, related_name='cover_letters')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cover_letters')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now= True)
    draft = models.BooleanField(default=True)

    tags = TaggableManager()

    def __str__(self):
        return self.title

    
#Create Dossier model here
class Dossier(models.Model):
  title = models.CharField(max_length=75)
  job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='dossiers')
  resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='dossiers',blank=True, null=True)
  cover_letter = models.ForeignKey(CoverLetter, on_delete=models.CASCADE, related_name='dossiers', blank=True, null=True)
  starrs = models.ManyToManyField(StarrQuestions, null=True, blank=True)
  questions = models.ManyToManyField(Question, null=True, blank=True)
  wins = models.ManyToManyField(Win, null=True, blank=True)
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dossiers', null=True, blank=True)
  created_at = models.DateTimeField(auto_now_add=True, null=True)
  updated_at = models.DateTimeField(auto_now= True, null=True)
  draft = models.BooleanField(default=True)
  tags = TaggableManager(blank=True)

  def __str__(self):
    return self.title

# Create Interview model here
class Interview(models.Model):
  title = models.CharField(max_length=75)
  job = models.ForeignKey(Job, null=True, on_delete=models.CASCADE, related_name='jobs')
  notes = models.TextField()
  date = models.DateField(null=True, blank=True, auto_now_add=False)
  time = models.TimeField(null=True, blank=True, auto_now_add=False)
  thank_you_letter = models.TextField()
  thank_you_letter_file = models.FileField(upload_to='thank_you_letter')
  questions_asked = models.TextField()
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='interviews')
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now= True)

  tags = TaggableManager(blank=True)

  def __str__(self):
    return self.title

# Create Goal model here
class Goal(models.Model):
  title = models.CharField(max_length=75)
  number = models.PositiveIntegerField()
  metric = models.CharField(max_length=50)
  date_to_complete = models.DateField(blank=True, null=True, auto_now_add=False)
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='goals')
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now= True)
  draft = models.BooleanField(default=True)

  tags = TaggableManager(blank=True)

  def __str__(self):
    return self.title

class ShortPersonalPitch(models.Model):
    title = models.CharField(max_length=75)
    user =  models.ForeignKey(User, on_delete=models.CASCADE, related_name='short_personal_pitch')
    pitch = models.TextField(max_length=650)
    draft = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now= True)
    tags = TaggableManager(blank=True)

    def __str__(self):
        return self.title

class LongPersonalPitch(models.Model):
    title = models.CharField(max_length=75)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='long_personal_pitch')
    pitch = models.TextField(max_length=1300)
    draft = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now= True)

    tags = TaggableManager(blank=True)

    def __str__(self):
        return self.title

class Links(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='links')
    title = models.CharField(max_length=75)
    link = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now= True)


    def __str__(self):
        return self.title

class CompanyComments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='company_comments')
    company = models.ForeignKey(TargetCompany, on_delete=models.CASCADE, related_name='company_comments')
    contact = models.ForeignKey(CompanyContacts, on_delete=models.CASCADE, related_name='comment_contact', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now= True)
    important_date = models.DateTimeField(blank=True, null=True)
    notes = models.TextField()


class JobComments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="job_comments")
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='job_comments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now= True)
    important_date = models.DateTimeField(blank=True,null=True)
    notes = models.TextField()